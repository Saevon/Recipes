import requests
import yaml


for page in range(1840, 2500):
    response = requests.get('https://subnautica.unknownworlds.com/api/time-capsules-voting-queue?page={}'.format(page))
    info = response.json()

    capsules = ''

    for capsule in info['capsules']:
        if capsule.get('user_name', '').lower() == 'saevon':
            print(capsule)
        # elif 'angle' in capsule['text']:
        #     print(capsule)
        encoded = yaml.dump(capsule, default_flow_style=False).split('\n')
        for index, line in enumerate(encoded):
            if index == 0:
                line = '- ' + line
            else:
                line = '  ' + line

            encoded[index] = '  ' + line

        capsules += '\n'.join(encoded)

    with open('capsules.yaml', 'a') as file_handle:
        file_handle.write(capsules)

    print(str(page) + ', ')



# dump(default_flow_style=False)
