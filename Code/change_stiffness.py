from naoqi import ALProxy

def convert_stiff_to_numeric(stiff):
    if stiff:
        return 0.0, 'Stiffening'
    else:
        return 1.0, 'Loosening'

if __name__ == '__main__':
    stiff = input("Enter True to stiffen, False to un-stiffen")
    if stiff not in [True, False]:
        raise ValueError('Input not allowed')

    stiff_numeric, confirm_text = convert_stiff_to_numeric(stiff)
    print('{} up'.format(confirm_text))

    motion = ALProxy("ALMotion", "192.168.1.3", 9559)
    motion.setStiffnesses("Body", stiff_numeric)