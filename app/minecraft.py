# see https://darkcoding.net/software/scripting-minecraft-server-with-python/
from mcpi.minecraft import Minecraft
import mcpi.block as block
import requests
import json

# look at this for getting users on the server
# create field for minecraft player name in moodle user profile extended profile attributes

def getPlayerEntityIds(self):
    """Get the entity ids of the connected players => [id:int]"""
    ids = self.conn.sendReceive(b"world.getPlayerIds")
    return list(map(int, ids.split("|")))

def getPlayerEntityId(self, name):
    """Get the entity id of the named player => [id:int]"""
    return int(self.conn.sendReceive(b"world.getPlayerId", name))


# get user id from Evoke site administration page
test_moodle_user_id = 2

# Making a get request
# 127.0.0.1 is localhost; update based on api server and port
r = requests.get(f'http://127.0.0.1:8000/moodle-badges-for-user/{test_moodle_user_id}')

# API returns data in bytes; decode and load into a Python dict representation of JSON
data = json.loads(r.content.decode('utf-8'))

# post response to Minecraft server
# minecraft server must have port 4711 open on firewall
# sudo ufw allow 4711
# sudo ufw enable and press Y when prompted
# server ip in server.properties on minecraft server must be 0.0.0.0 to allow remote connections
minecraft_server = "192.168.1.32"
minecraft_server_port = 4711
mc = Minecraft.create(minecraft_server, minecraft_server_port)

# get user ids
result = mc.getPlayerEntityIds()


# message to post to Moodle chat
chat_message = f'This is an Urgent EVOKE from Alchemy... LET THERE BE LIGHT - {data["badgeOwnerMoodleId"]} earned the {data["badgeName"]} badge!'

# post to chat expects string
mc.postToChat(chat_message)

# additional user feedback
print(f'Posted "{chat_message}" to minecraft server running on {minecraft_server} port {minecraft_server_port}')

# get list of Minecraft users
try:
    result = mc.getPlayerEntityIds()
    print(f'Minecraft Players: {result}')
    print(f'Player 1 position: {mc.entity.getPos(result[0])}')
except:
    print('Unable to get user list. Are any users logged in?')

playerId = result[0]

# player position
x, y, z = mc.entity.getPos(playerId)

# feedback
print(mc.entity.getName(playerId))

# place block based on badge; if badges exist for these then will appear in world next to specified user
# consider using BLOCK NAME for BADGE NAME so we can eaisily pass it through, eg data["badgeName"] aligned with block.[ENUM]
badgeName = data["badgeName"]
if badgeName == 'MEGA TORCH':
    mc.setBlock(x+1, y+1, z+1, block.TORCH )

if badgeName == 'CHEST':
    mc.setBlock(x-1, y-1, z+1, block.CHEST )



# showing an example of an entity in the world
# other functions
try:
    result = mc.getEntities()
    print(f'Minecraft Entities: {result[0]}')
except:
    print('Request failed.')