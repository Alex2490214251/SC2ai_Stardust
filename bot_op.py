from abc import ABC

from start import *
from sc2.constants import UnitTypeId, AbilityId, BuffId
import random


class bot_op(bot_api):

    def __init__(self):
        super().__init__()
        self.set_1 = []
        self.set_2 = []

    async def bot_op(self):
        await self.op_building()
        await self.op_army()

    async def op_building(self):
        await self.operation_nexus()
        if self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
            await self.operation_cyberneticscore()
        if self.structures(UnitTypeId.TWILIGHTCOUNCIL).ready.exists:
            await self.operation_twilightcouncil()
        await self.operation_forge()
        if self.structures(UnitTypeId.ROBOTICSBAY).ready.exists:
            await self.operation_roboticsbay()
        if self.structures(UnitTypeId.TEMPLARARCHIVE).ready.exists:
            await self.operation_templararchive()

    async def op_army(self):
        # await self.att_control()
        await self.att_control()
        await self.operation_stalker()
        await self.operation_sentry()
        await self.operation_hightemplar()
        await self.operation_observer()
        await self.scout()

    async def operation_cyberneticscore(self):
        cyberneticscore = self.structures(UnitTypeId.CYBERNETICSCORE).ready.first
        if cyberneticscore.is_idle:
            if self.can_afford(AbilityId.RESEARCH_WARPGATE) and \
                    await self.has_ability(AbilityId.RESEARCH_WARPGATE, cyberneticscore):
                self.do(cyberneticscore(AbilityId.RESEARCH_WARPGATE))

    async def operation_twilightcouncil(self):
        twilightcouncil = self.structures(UnitTypeId.TWILIGHTCOUNCIL).ready.first
        if twilightcouncil.is_idle:
            if await self.has_ability(AbilityId.RESEARCH_BLINK, twilightcouncil):
                if self.can_afford(AbilityId.RESEARCH_BLINK):
                    self.do(twilightcouncil(AbilityId.RESEARCH_BLINK))
            elif await self.has_ability(AbilityId.RESEARCH_CHARGE, twilightcouncil):
                if self.can_afford(AbilityId.RESEARCH_CHARGE):
                    self.do(twilightcouncil(AbilityId.RESEARCH_CHARGE))

    async def operation_templararchive(self):
        templararchive = self.structures(UnitTypeId.TEMPLARARCHIVE).ready.first
        if templararchive.is_idle:
            if await self.has_ability(AbilityId.RESEARCH_PSISTORM, templararchive):
                if self.can_afford(AbilityId.RESEARCH_PSISTORM):
                    self.do(templararchive(AbilityId.RESEARCH_PSISTORM))

    async def operation_forge(self):
        att_1 = AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1
        att_2 = AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL2
        att_3 = AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL3
        def_1 = AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1
        def_2 = AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL2
        def_3 = AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL3
        shd_1 = AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1
        shd_2 = AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL2
        shd_3 = AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL3
        for forge in self.structures(UnitTypeId.FORGE).ready.idle:
            if await self.has_ability(att_1, forge):
                if self.can_afford(att_1):
                    self.do(forge(att_1))
            elif await self.has_ability(def_1, forge):
                if self.can_afford(def_1):
                    self.do(forge(def_1))
            elif await self.has_ability(att_2, forge):
                if self.can_afford(att_2):
                    self.do(forge(att_2))
            elif await self.has_ability(def_2, forge):
                if self.can_afford(def_2):
                    self.do(forge(def_2))
            elif await self.has_ability(att_3, forge):
                if self.can_afford(att_3):
                    self.do(forge(att_3))
            elif await self.has_ability(def_3, forge):
                if self.can_afford(def_3):
                    self.do(forge(def_3))
            elif await self.has_ability(shd_1, forge):
                if self.can_afford(shd_1):
                    self.do(forge(shd_1))
            elif await self.has_ability(shd_2, forge):
                if self.can_afford(shd_2):
                    self.do(forge(shd_2))
            elif await self.has_ability(shd_3, forge):
                if self.can_afford(shd_3):
                    self.do(forge(shd_3))

    async def operation_roboticsbay(self):
        roboticsbay = self.structures(UnitTypeId.ROBOTICSBAY).ready.first
        if roboticsbay.is_idle:
            if await self.has_ability(AbilityId.RESEARCH_EXTENDEDTHERMALLANCE, roboticsbay):
                if self.can_afford(AbilityId.RESEARCH_EXTENDEDTHERMALLANCE):
                    self.do(roboticsbay(AbilityId.RESEARCH_EXTENDEDTHERMALLANCE))

    async def operation_nexus(self):

        working_structures = self.working(UnitTypeId.FORGE) + \
                             self.working(UnitTypeId.TWILIGHTCOUNCIL) + \
                             self.working(UnitTypeId.TEMPLARARCHIVE) + \
                             self.working(UnitTypeId.ROBOTICSFACILITY) + \
                             self.working(UnitTypeId.CYBERNETICSCORE)

        for nexus in self.structures(UnitTypeId.NEXUS).ready:
            if await self.has_ability(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus):
                if len(working_structures) > 0:
                    for a in range(len(working_structures)):
                        if not working_structures[a].has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                            self.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST,working_structures[a]))

    async def operation_stalker(self):
        for stalker in self.units(UnitTypeId.STALKER):
            if stalker in self.set_1:
                if await self.has_ability(AbilityId.EFFECT_BLINK_STALKER, stalker):
                    if stalker.shield_percentage <= 0.4 and await self.in_combat(stalker):
                        self.do(stalker(
                            AbilityId.EFFECT_BLINK_STALKER,
                            self.enemy_units.closest_to(stalker.position).position.towards(
                                stalker.position, 14
                            )))

    async def operation_sentry(self):

        shd_ex = False

        for sentry in self.units(UnitTypeId.SENTRY):
            if sentry.has_buff(BuffId.GUARDIANSHIELD):
                shd_ex = True

        for sentry in self.units(UnitTypeId.SENTRY):
            if await self.in_combat(sentry):
                if await self.has_ability(AbilityId.GUARDIANSHIELD_GUARDIANSHIELD, sentry) and sentry.energy >= 75:
                    if await self.in_combat(sentry) and not shd_ex:
                        self.do(sentry(AbilityId.GUARDIANSHIELD_GUARDIANSHIELD))
                        break

    async def operation_hightemplar(self):

        en_u = self.enemy_units.filter(lambda unit: unit.energy_percentage > 0.8 and unit.energy_max >= 100)
        en_e = self.units(UnitTypeId.HIGHTEMPLAR).filter(lambda unit: unit.energy < 45)

        for hightemplar in self.units(UnitTypeId.HIGHTEMPLAR):
            if await self.in_combat(hightemplar):
                if hightemplar.energy > 75:
                    if await self.has_ability(AbilityId.PSISTORM_PSISTORM, hightemplar):
                        self.do(hightemplar(AbilityId.PSISTORM_PSISTORM,
                                            self.enemy_units.closest_to(hightemplar.position).position.towards(
                                                hightemplar.position, -2
                                            )))
                        break
                elif hightemplar.energy > 50:
                    if len(en_u) > 0:
                        self.do(hightemplar(AbilityId.FEEDBACK_FEEDBACK,
                                            self.enemy_units.filter(
                                                lambda unit: unit.energy_percentage > 0.8 and
                                                             unit.energy_max >= 100).closest_to(hightemplar)))
                        break

        if len(en_e) >= 2:
            ht_1 = en_e[0]
            ht_2 = en_e[1]
            self.do(ht_1(AbilityId.MORPH_ARCHON))
            self.do(ht_2(AbilityId.MORPH_ARCHON))

    async def scout(self):

        u_ig = [UnitTypeId.DRONE,
                UnitTypeId.SCV,
                UnitTypeId.PROBE,
                UnitTypeId.EGG,
                UnitTypeId.LARVA,
                UnitTypeId.OVERLORD,
                UnitTypeId.OVERSEER,
                UnitTypeId.OBSERVER]

        u_det = [UnitTypeId.OBSERVER,
                 UnitTypeId.PHOTONCANNON,
                 UnitTypeId.OVERSEER,
                 UnitTypeId.RAVEN,
                 UnitTypeId.MISSILETURRET,
                 UnitTypeId.SPORECRAWLER,
                 UnitTypeId.SPORECANNON]

        if self.units(UnitTypeId.PROBE).ready.amount > 22 and self.units(UnitTypeId.OBSERVER).ready.amount == 0:
            scout_worker = None
            for worker in self.workers:
                if self.has_order([AbilityId.PATROL], worker):
                    scout_worker = worker
            if not scout_worker:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                scout_worker = self.workers.closest_to(self.start_location)
                if not scout_worker:
                    return
                await self.order(scout_worker, AbilityId.PATROL, random_exp_location)
                return
            nearby_enemy_units = self.enemy_units.filter(lambda unit: unit.type_id not in u_ig).closer_than(10,
                                                                                                            scout_worker)
            if nearby_enemy_units.exists:
                await self.order(scout_worker, AbilityId.PATROL, self.game_info.map_center)
                return
            target = (scout_worker.orders[0].target.x, scout_worker.orders[0].target.y)
            if scout_worker.distance_to(target) < 10:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                await self.order(scout_worker, AbilityId.PATROL, random_exp_location)
                return

        if self.units(UnitTypeId.OBSERVER).ready.amount > 1:
            scout = None
            for observer in self.units(UnitTypeId.OBSERVER):
                if self.has_order([AbilityId.PATROL], observer):
                    scout = observer
            if not scout:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                scout = self.units(UnitTypeId.OBSERVER).closest_to(self.start_location)
                if not scout:
                    return
                await self.order(scout, AbilityId.PATROL, random_exp_location)
                return
            if self.enemy_units.filter(lambda unit: unit.type_id in u_det).closer_than(11, scout):
                await self.order(scout, AbilityId.PATROL, self.game_info.map_center)
                return
            target = (scout.orders[0].target.x, scout.orders[0].target.y)
            if scout.distance_to(target) < 10:
                random_exp_location = random.choice(list(self.expansion_locations.keys()))
                await self.order(scout, AbilityId.PATROL, random_exp_location)
                return

    async def operation_observer(self):
        for observer in self.units(UnitTypeId.OBSERVER).idle:
            if self.units(UnitTypeId.STALKER).ready.exists:
                self.do(
                    observer.move(self.units(UnitTypeId.STALKER).closest_to(self.enemy_start_locations[0]).position.
                                  towards(self.start_location, 4)))

    async def att_control(self):

        f2 = []

        trp = [UnitTypeId.ZEALOT,
               UnitTypeId.STALKER,
               UnitTypeId.SENTRY,
               UnitTypeId.IMMORTAL,
               UnitTypeId.COLOSSUS,
               UnitTypeId.HIGHTEMPLAR,
               UnitTypeId.ARCHON]
        for t in trp:
            for u in self.units(t).ready:
                f2.append(u)
                if u not in self.set_1 and u not in self.set_2:
                    self.set_2.append(u)

        if len(self.set_2) > 42:
            self.set_1 = self.set_2
            self.set_2 = []
        if len(self.set_1) < 10:
            self.set_2 += self.set_1
            self.set_1 = []
        if len(self.set_1) > 32:
            if len(self.set_2) > 8:
                self.set_1 += self.set_2
                self.set_2 = []

        for a in self.set_1:
            if a not in f2:
                self.set_1.remove(a)
        for b in self.set_2:
            if b not in f2:
                self.set_2.remove(b)

        for trp in f2:
            if trp in self.set_1:
                await self.macro_attack(trp)
            else:
                await self.macro_defend(trp)
