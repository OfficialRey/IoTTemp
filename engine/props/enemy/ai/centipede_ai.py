from engine.props.enemy.ai.ai import MeleeAI
from engine.props.enemy.storage.centipede.centipede_body import CentipedeBody
from engine.props.enemy.storage.centipede.centipede_head import CentipedeHead


class CentipedeAI(MeleeAI):

    def __init__(self, entity):
        super().__init__(entity)

    def _run_ai(self, world, delta_time: float):
        super()._run_ai(world, delta_time)
        for segment in self.entity.segments:
            segment.update(world, delta_time)
        self.remove_dead_segments()

    def remove_dead_segments(self):
        to_remove = []
        for segment in self.entity.segments:
            if segment.can_remove():
                to_remove.append(segment)

        if len(to_remove) > 0:
            for removable in to_remove:
                self.entity.segments.remove(removable)
        self.split_centipede()

    def split_centipede(self):
        for i in range(len(self.entity.segments)):
            current_segment = self.entity.segments[i]
            if isinstance(current_segment, CentipedeBody):
                # Create new head
                if not current_segment.is_dead() and not current_segment.has_head():
                    self.entity.segments[i] = CentipedeHead(self.entity.sound_engine, self, self.entity.head_texture,
                                                            current_segment.center_position)
                    if i + 1 < len(self.entity.segments):
                        self.entity.segments[i + 1].previous_segment = self.entity.segments[i]
