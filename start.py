from sc2.constants import UnitTypeId,AbilityId

from bot_api import bot_api

class start(bot_api):
    async def two_base(self):
        if self.structures(UnitTypeId.NEXUS).exists:

            pylon_position = self.structures(UnitTypeId.NEXUS).first.position.towards(self.game_info.map_center,9.2)

            if self.supply_workers < 14:
                await self.train_(UnitTypeId.PROBE,UnitTypeId.NEXUS)
            elif self.supply_workers == 14 and await self.count_building(UnitTypeId.PYLON) < 1:
                await self.build_(UnitTypeId.PYLON,pylon_position)
            elif self.supply_workers < 16:
                await self.train_(UnitTypeId.PROBE,UnitTypeId.NEXUS)
            if self.structures(UnitTypeId.PYLON).ready.exists:
                nexus = self.structures(UnitTypeId.NEXUS).ready.first
                if not nexus.is_idle:
                    self.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus))
            if self.structures(UnitTypeId.GATEWAY).exists:
                if self.supply_workers < 19:
                    await self.train_(UnitTypeId.PROBE, UnitTypeId.NEXUS)
                elif self.supply_workers == 19:
                    if self.can_afford(UnitTypeId.NEXUS):
                        await self.expand_now()
                    if self.structures(UnitTypeId.PYLON).ready.exists and self.structures(UnitTypeId.NEXUS).amount > 1:
                        if not self.structures(UnitTypeId.CYBERNETICSCORE) and not self.already_pending(UnitTypeId.CYBERNETICSCORE):
                            pylon = self.structures(UnitTypeId.PYLON).ready.random
                            await self.build_(UnitTypeId.CYBERNETICSCORE, pylon)
            if self.structures(UnitTypeId.CYBERNETICSCORE).exists:
                if self.supply_workers < 20:
                    await self.train_(UnitTypeId.PROBE, UnitTypeId.NEXUS)
                elif self.supply_workers == 20 and await self.count_building(UnitTypeId.ASSIMILATOR) < 2:
                    await self.build_assimilator_()
                elif self.supply_workers < 21:
                    await self.train_(UnitTypeId.PROBE, UnitTypeId.NEXUS)
                elif self.supply_workers == 21 and await self.count_building(UnitTypeId.PYLON) < 2:
                    await self.build_(UnitTypeId.PYLON, pylon_position)
                elif await self.count_building(UnitTypeId.PYLON) == 2:
                    await self.train_(UnitTypeId.PROBE, UnitTypeId.NEXUS)

            if self.structures(UnitTypeId.PYLON).ready.exists:
                if not self.structures(UnitTypeId.GATEWAY).exists and not self.already_pending(UnitTypeId.GATEWAY):
                    pylon = self.structures(UnitTypeId.PYLON).ready.random
                    await self.build_(UnitTypeId.GATEWAY, pylon)
            if self.structures(UnitTypeId.GATEWAY).exists and await self.count_building(UnitTypeId.ASSIMILATOR) < 1:
                await self.build_assimilator_()
















