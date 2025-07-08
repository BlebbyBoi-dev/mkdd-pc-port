class AnimationObject:
    def __init__(self):
        self.weight = [0.0] * 4
        self.frame = 0
        self.flags = 1  # Assume animation is always looping

    def reset_frame(self):
        self.frame = 0

    def set_weight(self, index, value):
        self.weight[index] = value

    def update_frame(self):
        self.frame += 1

class AnmControlTrans:
    def __init__(self, max_anm_no):
        self.mMaxAnmNo = max_anm_no
        self.mObj = [AnimationObject() for _ in range(max_anm_no)]
        self.mNowAnmNo = 0
        self._1c = 0
        self._1d = 0
        self._1e = 0
        self._1f = 0
        self.mFlags = 0

    def change_blend_anm(self, anm_no, p2, p3):
        if anm_no != self.mNowAnmNo:
            self._1c = anm_no
            self._1d = 0
            self._1e = p2
            self._1f = p3
            self.mFlags |= 2
            self.mObj[self._1c].reset_frame()

    def doframe(self, anm_no):
        self.mObj[anm_no].update_frame()

    def change_anm(self, anm_no):
        self.mNowAnmNo = anm_no

    def frame_proc(self):
        self.doframe(self.mNowAnmNo)

        if self.mFlags & 2:
            if self._1d > self._1e:
                self.change_anm(self._1c)
                if self.mObj[self._1c].flags & 1:
                    self.mObj[self._1c].set_weight(0, 1.0)
                    for i in range(1, 4):
                        self.mObj[self._1c].set_weight(i, 0.0)
                self.mFlags &= ~2
            else:
                self.doframe(self._1c)
                tmp = self._1d / self._1e
                self.mObj[self.mNowAnmNo].set_weight(0, 1.0 - tmp)
                self.mObj[self.mNowAnmNo].set_weight(self._1f, tmp)
                self._1d += 1
        else:
            if self.mObj[self.mNowAnmNo].flags & 1:
                self.mObj[self.mNowAnmNo].set_weight(0, 1.0)
                for i in range(1, 4):
                    self.mObj[self.mNowAnmNo].set_weight(i, 0.0)

# === ACTUALLY RUNNING THE SIMULATION ===
trans = AnmControlTrans(2)

print("Starting animation 0...")
for i in range(5):
    trans.frame_proc()
    print(f"Frame {i} - Weights: {trans.mObj[0].weight}")

print("\nBlending to animation 1...")
trans.change_blend_anm(1, 5, 1)

for i in range(7):
    trans.frame_proc()
    print(f"Frame {i+5} - Weights: A0 {trans.mObj[0].weight} | A1 {trans.mObj[1].weight}")
