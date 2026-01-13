from importlib import reload
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()
ground = Entity(model='plane', scale=64, texture='brick', collider='box', position=(0, 0, 0))
player = FirstPersonController()
player.scale_y = 0.8

# Defining Starting Variables

shooting = False
main_ammo = 30
second_ammo = 10
ammo = main_ammo
gun = 1
running = False
wall1 = []
reloading = False
start_time = time.time()

# Sky
Sky()

# House 1 Building

for i in range(13):
    for j in range(8):
        block = Entity(model="cube", position=(i + 2, j + 0.5, 5), collider="box", texture="brick", color=color.brown)
        wall1.append(block)

# Text

reload_text = Text('RELOAD', scale=2, position=(-0.1,-0.3), enabled=False)
reloading_text = Text(text='Reloading', scale=2, position=(-0.1,-0.3), enabled=False)
ammo_text = Text(text=f'Ammo: {ammo}', position=(-0.85,0.45), scale=2)
coordinate_text = Text(text='', position=(-0.85,0.4), scale=2)
gun_text = Text(text=f'Gun: {gun}', enabled=True)

def show_reload():
    reload_text.enabled = True
    invoke(hide_reload, delay=1)  # call hide_reload after 1 second

def hide_reload():
    reload_text.enabled = False

def show_reloading(gun):
    global reloading
    reloading_text.enabled = True
    reloading = True
    if gun == 1:
        invoke(hide_reloading, delay=3)
    else:
        invoke(hide_reloading, delay=1.5)

def hide_reloading():
    global reloading
    reloading = False
    reloading_text.enabled = False

def add_ammo(gun):
    global main_ammo
    main_ammo = 30
    print(f'Gun {gun} is reloading')

def set_ammo():
    global second_ammo
    second_ammo = 10
    print(f"Ammo set to {second_ammo}")

# Shooting Mechanism

def input(key):
    global shooting, ammo, running, gun, main_ammo, second_ammo, reloading
    if key == "right mouse down":
        if gun == 1 and main_ammo > 0:  # Check for ammo of the specific gun
            fire()
        elif gun == 1 and main_ammo == 0:
            show_reload()  # Show reload message if out of ammo for Gun 1
        elif gun == 2 and second_ammo > 0:  # Check for ammo of the specific gun
            fire()
        elif gun == 2 and second_ammo == 0:
            show_reload()  # Show reload message if out of ammo for Gun 2

    if key == 'p':
        sys.exit()

    if key == "shift":
        if not running:
            player.speed *= 2
            running = True
        else:
            player.speed *= 0.5
            running = False

    if key == "1":  # Whatever
        gun = 1
        print('gun is 1')

    if key == "2":  # Pistol Pew Pew
        gun = 2
        print('gun is 2')
    if key == "r":  # Reloading Pew Pew
        if gun == 1:
            if main_ammo < 30:
                if not reloading:
                    show_reloading(1)
                    reloading = True
                    main_sequence.start()
                    print('Reloading Gun 1')
                    reloading = False# Ammo added after 3 seconds
        else:  # Gun 2 reloading
            if second_ammo < 10:
                if not reloading:
                    show_reloading(2)
                    reloading = True
                    second_sequence.start()
                    print('Reloading Gun 2')
                    reloading = False# Ammo added after 1.5 seconds


# Fire Mechanic

def fire():
    global ammo, main_ammo, second_ammo
    if gun == 1:
        main_ammo -= 1
    else:
        second_ammo -= 1

# Sequences

main_sequence = Sequence(
                            Wait(3),
                            Func(add_ammo, 1)
                    )

second_sequence = Sequence(
                            Wait(1.5),
                            Func(set_ammo)
                        )

# Update Loop

def update():
    global ammo, gun, main_ammo, second_ammo, start_time
    ammo_text.text = f'Ammo: {ammo}'
    gun_text.text = f'Gun: {gun}'
    coordinate_text.text = f'X: {player.x:.2f}, Y: {player.y:.2f}, Z: {player.z:.2f}'
    if gun == 1:
        ammo = main_ammo
    else:
        ammo = second_ammo
    seconds_elapsed = int(time.time() - start_time)
    print(f"Seconds elapsed: {seconds_elapsed}", end='\r')

app.run()