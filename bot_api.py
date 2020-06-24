from sc2 import *
from sc2 import position
from sc2.constants import UnitTypeId, AbilityId
from sc2 import BotAI


class bot_api(BotAI):

    def __init__(self):

        super().__init__()
        self.mov_dis = {
            UnitTypeId.ZEALOT: 0,
            UnitTypeId.STALKER: 8,
            UnitTypeId.SENTRY: 8,
            UnitTypeId.IMMORTAL: 7,
            UnitTypeId.COLOSSUS: 11,
            UnitTypeId.HIGHTEMPLAR: 7,
            UnitTypeId.ARCHON: 4
        }

    async def has_ability(
            self,
            ability: AbilityId,
            unit):
        unit_ability = await self.get_available_abilities(unit)
        if ability in unit_ability:
            return True
        else:
            return False

    def has_order(self,
                  orders,
                  unit):
        if type(orders) != list:
            orders = [orders]
        count = 0
        if len(unit.orders) >= 1 and unit.orders[0].ability.id in orders:
            count += 1
        return count

    async def train_(
            self,
            unit: UnitTypeId,
            building: UnitTypeId
    ):
        if self.structures(building).ready.exists:
            for building in self.structures(building).ready.idle:
                if self.can_afford(unit):
                    self.do(building.train(unit))
                    break

    async def warp_in(self,
                      unit: UnitTypeId,
                      location=None):
        import random
        x = random.randrange(-8, 8)
        y = random.randrange(-8, 8)
        for warpgate in self.structures(UnitTypeId.WARPGATE).ready.idle:
            if self.structures(UnitTypeId.PYLON).ready.exists:
                if location == None:
                    position_point = self.structures(UnitTypeId.PYLON).ready.random.position
                    placement = position.Point2((position_point.x + x, position_point.y + y))
                else:
                    placement = position.Point2((location.x + x, location.y + y))
                if self.can_afford(unit):
                    self.do(warpgate.warp_in(unit, placement))

    async def build_(
            self,
            building: UnitTypeId,
            position
    ):
        if self.can_afford(building):
            await self.build(building, near=position)

    async def order(self,
                    units,
                    order,
                    target=None):
        if type(units) != list:
            unit = units
            self.do(unit(order, target=target))
        else:
            for unit in units:
                self.do(unit(order, target=target))

    async def count_building(self, building: UnitTypeId):  # For buildings
        ready = self.structures(building).ready.amount
        pending = self.already_pending(building)
        if building == UnitTypeId.GATEWAY or building == UnitTypeId.WARPGATE:
            ready = self.structures(UnitTypeId.GATEWAY).ready.amount + self.structures(UnitTypeId.WARPGATE).ready.amount
            pending = self.already_pending(UnitTypeId.GATEWAY) + self.already_pending(UnitTypeId.WARPGATE)
        return ready + pending

    async def count_unit(self, unit: UnitTypeId):  # For units
        ready = self.units(unit).ready.amount
        pending = self.already_pending(unit)
        return ready + pending

    async def build_assimilator_(self):

        global Vespene

        if self.structures(UnitTypeId.NEXUS).ready.exists:
            for Nexus in self.structures(UnitTypeId.NEXUS).ready:
                Vespene = self.vespene_geyser.closer_than(9.0, Nexus).filter \
                    (lambda vaspene: not self.structures(UnitTypeId.ASSIMILATOR).closer_than(0.5, vaspene.position))
        for vespene in Vespene:
            worker = self.units(UnitTypeId.PROBE).ready.closest_to(vespene.position)
            if worker != None and self.can_afford(UnitTypeId.ASSIMILATOR):
                self.do(worker.build(UnitTypeId.ASSIMILATOR, vespene))
                break

    async def macro_attack(self, trp):

        if trp.weapon_cooldown != 0 or trp.is_attacking:
            if len(self.threat()) > 0:
                self.do(trp.move(self.threat().closest_to(trp.position).position.towards(
                    trp.position,
                    self.mov_dis[trp.type_id]
                )))
            else:
                await self.push(trp)
        else:
            if len(self.threat()) > 0:
                self.do(trp.attack(self.threat().closest_to(trp.position)))
            else:
                await self.push(trp)

    async def macro_defend(self, trp):

        hf_mp = self.start_location.position.distance_to(self.enemy_start_locations[0].position)

        enemy_attack = self.threat().filter(lambda unit: unit.distance_to(self.start_location) < 0.5 * hf_mp) + \
                       self.enemy_structures.filter(lambda unit: unit.distance_to(self.start_location) < 0.5 * hf_mp)

        rally_position = self.structures(UnitTypeId.PYLON).ready.closest_to(self.enemy_start_locations[0]). \
            position.towards(self.game_info.map_center, 5)

        if len(enemy_attack) > 0:
            if trp.weapon_cooldown != 0 or trp.is_attacking:
                if self.threat().exists:
                    self.do(trp.move(self.threat().closest_to(trp.position).position.towards(
                        trp.position,
                        self.mov_dis[trp.type_id]
                    )))
                else:
                    self.do(trp.move(self.enemy_structures.closest_to(trp.position).position.towards(
                        trp.position,
                        self.mov_dis[trp.type_id]
                    )))
            else:
                if self.threat().exists:
                    self.do(trp.attack(self.threat().closest_to(trp.position)))
                else:
                    self.do(trp.attack(self.enemy_structures.closest_to(trp.position)))
        else:
            if trp.distance_to(rally_position) > 10:
                self.do(trp.move(rally_position))

    async def warp(self):
        if self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
            cyberneticscore = self.structures(UnitTypeId.CYBERNETICSCORE).first
            if not await self.has_ability(AbilityId.RESEARCH_WARPGATE, cyberneticscore):
                return True
        return False

    async def in_combat(self, unit):
        in_r = []
        for e in self.threat():
            if e.distance_to(unit) <= 11:
                in_r.append(e)
        return len(in_r) > 5

    def threat(self):

        u_ig = [UnitTypeId.EGG,
                UnitTypeId.LARVA,
                UnitTypeId.OVERLORD,
                UnitTypeId.OBSERVER]

        tur = [UnitTypeId.PHOTONCANNON,
               UnitTypeId.MISSILETURRET,
               UnitTypeId.SPORECANNON,
               UnitTypeId.SPINECRAWLER]

        e = self.enemy_units.filter(lambda unit: unit.type_id not in u_ig)
        t = self.enemy_structures.filter(lambda unit: unit.type_id in tur)
        return e + t

    def working(self, buildings: UnitTypeId):
        idle = self.structures(buildings).idle
        return self.structures(buildings) - idle

    async def push(self, trp):
        if len(self.enemy_structures) > 0:
            self.do(trp.attack(self.enemy_structures.closest_to(trp.position)))
        else:
            self.do(trp.attack(self.enemy_start_locations[0]))
