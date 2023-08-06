import yaml

from tinder_cli.client import TinderClient


class TinderCLI(object):
    client = TinderClient()
    commands = ('like', 'superlike', 'pass', 'info', 'meta', 'teasers', 'profile')
    profile_keys = ('bio', 'birth_date', 'gender', 'distance_mi', 'jobs', 'name', 'photos', 'instagram', 'schools')

    def __init__(self, tinder_token):
        self.session = self.client.get_session(tinder_token)

    def run(self, cmd, tinder_id):
        if cmd == 'info':
            return self.cmd_info(tinder_id)

        elif cmd == 'like':
            return self.cmd_like(tinder_id)

        elif cmd == 'pass':
            return self.cmd_pass(tinder_id)

        elif cmd == 'superlike':
            return self.cmd_superlike(tinder_id)

        elif cmd == 'profile':
            return self.cmd_profile()

        elif cmd == 'teasers':
            return self.cmd_teasers()

    def cmd_info(self, tinder_id):
        tinder_id = self.get_tinder_id(tinder_id)

        resp = self.client.get_user(self.session, tinder_id)
        resp.raise_for_status()

        data = {k: v for k, v in resp.json().get('results', {}).items() if k in self.profile_keys}

        data.update({
            'birth_year': int(data.pop('birth_date')[:4]),
            'photos': [x['url'] for x in data['photos']],
            'gender': 'F' if data['gender'] == 1 else 'M' if data['gender'] == 0 else 'O'
        })

        if 'jobs' in data and len(data['jobs']) == 0:
            data.pop('jobs')

        if 'schools' in data and len(data['schools']) == 0:
            data.pop('schools')

        if 'instagram' in data:
            data['instagram'] = [x['image'] for x in data['instagram'].get('photos', [])]

        return yaml.dump(data)

    def cmd_profile(self):
        resp = self.client.get_profile(self.session)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    def cmd_teasers(self):
        resp = self.client.get_teasers(self.session)
        resp.raise_for_status()

        profiles = []

        for item in resp.json().get('data', {}).get('results', []):
            for photo in item.get('user', {}).get('photos', []):
                profiles.append({'image_id': photo['id'], 'url': photo['url']})

        return yaml.dump(profiles)

    def cmd_like(self, tinder_id):
        tinder_id = self.get_tinder_id(tinder_id)

        resp = self.client.like_user(self.session, tinder_id)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    def cmd_superlike(self, tinder_id):
        tinder_id = self.get_tinder_id(tinder_id)

        resp = self.client.superlike_user(self.session, tinder_id)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    def cmd_pass(self, tinder_id):
        tinder_id = self.get_tinder_id(tinder_id)

        resp = self.client.pass_user(self.session, tinder_id)
        resp.raise_for_status()

        return yaml.dump(resp.json())

    @staticmethod
    def get_tinder_token(token=False):
        return input('input your tinder token: ').strip() if not token else token

    @staticmethod
    def get_tinder_id(tinder_id=False):
        return input('input tinder id: ').strip() if not tinder_id else tinder_id
