from naoqi import ALProxy


def get_input():
    stiff = input("Stiffen or unstiffen? \n")
    return stiff


def change_stiffness(stiffness, part):
    if stiffness in ['stiffen', 'Stiffen', 'stiff', 'Stiff']:
        motion.setStiffnesses(part, 1.0)
        return 'Stiffening'
    else:
        motion.setStiffnesses(part, 0.0)
        return 'Loosening'


if __name__ == '__main__':
    motion = ALProxy("ALMotion", "192.168.1.3", 9559)

    stiffness = get_input()
    confirm_text = change_stiffness(stiffness, "Body")
    print('{} up'.format(confirm_text))
