from math import pi, sin, cos  # Digunakan dalam menggerakkan kamera
# untuk mengambil dan menampilkan image dari framework ShowBase.
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3  # untuk mengatur arah koordinat aktor
from panda3d.core import ClockObject
from direct.task import Task
from direct.actor.Actor import Actor  # import kelas aktor yang akan digunakan.
from direct.interval.IntervalGlobal import Sequence

# untuk mengarahkan kunci bergerak keatas,bawah,sampingkiri,dan kanan

keyMap = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "rotate": False
}

# untuk memanggil kembali fungsi untuk memperbarui peta kunci


def updateKeyMap(key, state):
    keyMap[key] = state


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)  # menginisialisasi modul ShowBase

        self.disableMouse()
        # memuat model lingkungan.
        self.scene = self.loader.loadModel("models/environment")
        # mengatur ulang model yang akan dirender.
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Tambahkan prosedur spinCameraTask ke pengelola tugas.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load dan ubah aktor panda.
        self.Panda = Actor("models/panda-model",
                           {"walk": "models/panda-walk4"})
        self.Panda.setScale(0.005, 0.005, 0.005)
        self.Panda.reparentTo(self.render)

        # Loop animasinya.
        self.Panda.loop("walk")

        # Membuat event sebagai arah yang akan ditekan melalui keyboard
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        # Memberi nilai Kecepatan serta arah
        self.speed=6
        self.angle=0  # secara default bernilai 0

        self.taskMgr.add(self.update, "update")

    # Tentukan prosedur untuk memindahkan kamera.
    def spinCameraTask(self, task):
        # angle degress untuk mencari sudut kamera, sedangkan angleRadians digunakan untuk mendapatkan nilai radian dari sudut kamera tersebut dan task.time mengembalikan nilai (float) yang menunjukkan berapa lama fungsi tugas ini telah berjalan sejak eksekusi pertama fungsi tersebut. Timer berjalan bahkan ketika fungsi tugas tidak dijalankan.
        angleDegrees=task.time * 6.0
        angleRadians=angleDegrees * (pi / 180.0)
        # fungsi awal pergerakan kamera dimulai sedangkan setHpr mengembalikan kamera ke koordinat semula
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def update(self, task):

        globalClock = ClockObject.getGlobalClock()

        dt = globalClock.getDt()

        pos = self.Panda.getPos()

        # Membuat beberapa pengaturan action sesuai keyMap yang sudah didaftarkan mulai dari posisinya speed nya dan clock timenya
        if keyMap["left"]:
            pos.x -= self.speed * dt
        if keyMap["right"]:
            pos.x += self.speed * dt
        if keyMap["up"]:
            pos.z += self.speed * dt
        if keyMap["down"]:
            pos.z -= self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1  # akan mengubah nilai angle pada baris 64 karena objek akan berputar
            self.Panda.setH(self.angle)

        self.Panda.setPos(pos)

        return task.cont


# inisialisasi Function MyApp() ke variabel app
app=MyApp()
# load Musik
mySound=app.loader.loadSfx("backsound.ogg")
# mutar Musik
mySound.play()
# Membuat Musik terus berulang
mySound.setLoop(True)
# Mengatur volume
mySound.setVolume(13)
# menjalankan aplikasi
app.run()
