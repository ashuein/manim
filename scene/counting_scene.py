from scene import Scene

from mobject import *
from animation import *
from region import *
from constants import *
from helpers import *

DEFAULT_COUNT_NUM_OFFSET = (SPACE_WIDTH - 1, SPACE_HEIGHT - 1, 0)
DEFAULT_COUNT_RUN_TIME   = 5.0

class CountingScene(Scene):
    def count(self, items, item_type = "mobject", *args, **kwargs):
        if item_type == "mobject":
            self.count_mobjects(items, *args, **kwargs)
        elif item_type == "region":
            self.count_regions(items, *args, **kwargs)
        else:
            raise Exception("Unknown item_type, should be mobject or region")
        return self

    def count_mobjects(
        self, mobjects, mode = "highlight",
        color = "red", 
        display_numbers = True,
        num_offset = DEFAULT_COUNT_NUM_OFFSET,
        run_time   = DEFAULT_COUNT_RUN_TIME):
        """
        Note, leaves final number mobject as "number" attribute

        mode can be "highlight", "show_creation" or "show", otherwise
        a warning is given and nothing is animating during the count
        """
        if len(mobjects) > 50: #TODO
            raise Exception("I don't know if you should be counting \
                             too many mobjects...")
        if len(mobjects) == 0:
            raise Exception("Counting mobject list of length 0")
        if mode not in ["highlight", "show_creation", "show"]:
            raise Warning("Unknown mode")
        frame_time = run_time / len(mobjects)
        if mode == "highlight":
            self.add(*mobjects)
        for mob, num in zip(mobjects, it.count(1)):
            if display_numbers:
                num_mob = tex_mobject(str(num))
                num_mob.center().shift(num_offset)
                self.add(num_mob)
            if mode == "highlight":
                original_color = mob.color
                mob.highlight(color)
                self.dither(frame_time)
                mob.highlight(original_color)
            if mode == "show_creation":
                self.animate(ShowCreation(mob, run_time = frame_time))
            if mode == "show":
                self.add(mob)
                self.dither(frame_time)
            if display_numbers:
                self.remove(num_mob)
        if display_numbers:
            self.add(num_mob)
            self.number = num_mob
        return self

    def count_regions(self, regions, 
                      mode = "one_at_a_time",
                      num_offset = DEFAULT_COUNT_NUM_OFFSET,
                      run_time   = DEFAULT_COUNT_RUN_TIME,
                      **unused_kwargsn):
        if mode not in ["one_at_a_time", "show_all"]:
            raise Warning("Unknown mode")
        frame_time = run_time / (len(regions))
        for region, count in zip(regions, it.count(1)):
            num_mob = tex_mobject(str(count))
            num_mob.center().shift(num_offset)
            self.add(num_mob)
            self.highlight_region(region)
            self.dither(frame_time)
            if mode == "one_at_a_time":
                self.reset_background()
            self.remove(num_mob)
        self.add(num_mob)
        self.number = num_mob
        return self