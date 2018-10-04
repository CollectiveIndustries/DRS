#
# Smart Lib - module for dealing with pySMART i/o 
#

try:
    from pySMART import Device
except ImportError:
    print("You will need run pip install -r requirements.txt to correctly import dependencies.")
    sys.exit(1)

#
# Passive drive check. not an actual SMART forground test.
#
def test_disks():

    try:
        data = {}
        failed_disks = []
        for device, name in DISKS.iteritems():
            disk = Device('/dev/{}'.format(device))

            data[name] = disk.assessment

            # log failed ones so we can alert
            if disk.assessment != 'PASS':
                failed_disks.append(device)

        sorted_data = collections.OrderedDict(sorted(data.items()))

        for name, reading in sorted_data.iteritems():
            print("{0}: {1}".format(name, reading))

        for device in failed_disks:
            print("WARNING! Disk: {0} - {1} did not pass smartcl assessment".format(device, DISKS[device]))

    except Exception as exception:
        print_exc()
        print("Failed to get sensor data: {0}".format(exception.message))

# https://www.thomas-krenn.com/en/wiki/SMART_tests_with_smartctl
# http://chrishannam.co.uk/archives/68

