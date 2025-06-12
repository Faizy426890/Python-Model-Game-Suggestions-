from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np 
import random

app = Flask(__name__)

game_map = {
    # Outdoor Sports (1-100)
    0: ("Frisbee", "Casual throwing game perfect for parks and beaches", 2),
    1: ("Badminton (Outdoor)", "Racket sport great for light breeze conditions", 2),
    2: ("Soccer", "Team sport requiring open space, good for moderate weather", 22),
    3: ("Beach Volleyball", "Best played on sunny days at the beach", 4),
    4: ("Table Tennis (Outdoor)", "Enjoy this fast-paced game when there's minimal wind and pleasant temperatures.", 2),
    5: ("Tennis", "Best played in clear weather with minimal wind.", 2),
    6: ("Basketball", "Great for clear days when you want some cardio outdoors.", 10),
    7: ("Baseball", "Classic American sport perfect for warm, clear days with friends.", 18),
    8: ("Cricket", "Traditional bat and ball game ideal for sunny afternoons.", 22),
    9: ("Ultimate Frisbee", "Fast-paced team sport combining football and frisbee elements.", 14),
    10: ("Volleyball", "Energetic team game perfect for parks and beaches.", 12),
    11: ("Flag Football", "Non-contact version of football great for all skill levels.", 12),
    12: ("Rugby", "Physical team sport best played in mild weather conditions.", 30),
    13: ("Field Hockey", "Fast-paced stick sport ideal for cooler temperatures.", 22),
    14: ("Lacrosse", "Dynamic team sport combining skills of multiple games.", 20),
    15: ("Softball", "Easier version of baseball perfect for casual gatherings.", 18),
    16: ("Kickball", "Childhood favorite that's fun for adults too.", 12),
    17: ("Capture the Flag", "Strategic team game perfect for large groups.", 20),
    18: ("Touch Rugby", "Gentler version of rugby suitable for mixed groups.", 14),
    19: ("Handball", "Fast-paced court game that can be played outdoors.", 14),
    20: ("Dodgeball", "Classic playground game that's fun for all ages.", 12),
    21: ("Spikeball", "Trendy beach game played with a circular net.", 4),
    22: ("Kan Jam", "Flying disc game where teams compete to score points.", 4),
    23: ("Rounders", "British bat-and-ball game similar to baseball.", 16),
    24: ("Netball", "Popular team sport especially in Commonwealth countries.", 14),
    25: ("Swimming", "Perfect for hot sunny days to cool off in the water.", 1),
    26: ("Water Polo", "Competitive swimming sport combining strategy and endurance.", 14),
    27: ("Synchronized Swimming", "Artistic water sport combining dance and swimming.", 8),
    28: ("Water Basketball", "Basketball played in swimming pools for extra fun.", 10),
    29: ("Pool Volleyball", "Volleyball adapted for swimming pool play.", 12),
    30: ("Water Aerobics", "Low-impact exercise perfect for hot weather.", 15),
    31: ("Diving", "Exciting water sport for those who love heights.", 1),
    32: ("Surfing", "Ride the waves on sunny beach days.", 1),
    33: ("Paddleboarding", "Peaceful water activity for calm weather.", 1),
    34: ("Water Tag", "Classic chase game made more fun in water.", 8),
    35: ("Hiking", "Ideal for clear days with comfortable temperatures.", 1),
    36: ("Cycling", "Best when it's not too windy and temperatures are mild.", 1),
    37: ("Jogging", "Good for mild temperature days with light breeze.", 1),
    38: ("Yoga in the Park", "Perfect for calm, sunny mornings in open spaces.", 1),
    39: ("Rock Climbing", "Challenging outdoor activity for clear, dry days.", 2),
    40: ("Skateboarding", "Urban sport perfect for mild weather conditions.", 1),
    41: ("Roller Skating", "Fun activity for smooth surfaces and good weather.", 1),
    42: ("Parkour", "Urban movement sport ideal for dry conditions.", 1),
    43: ("Trail Running", "Running in nature, perfect for moderate temperatures.", 1),
    44: ("Outdoor Fitness Bootcamp", "High-intensity group workout in fresh air.", 12),
    45: ("Bocce Ball", "A relaxed ball game best played on grass or sand, perfect for good weather.", 4),
    46: ("Cornhole", "A perfect lawn game for gatherings in mild weather conditions.", 4),
    47: ("Horseshoes", "Traditional throwing game great for backyards.", 4),
    48: ("Croquet", "Elegant lawn game perfect for sunny afternoons.", 4),
    49: ("Mini Golf", "A fun outdoor activity that works in various weather conditions.", 4),
    50: ("Disc Golf", "Golf with frisbees through wooded courses.", 4),
    51: ("Lawn Bowling", "Precision sport played on grass in pleasant weather.", 8),
    52: ("Petanque", "French ball game similar to bocce, great for parks.", 4),
    53: ("Giant Jenga", "Oversized version of the classic stacking game.", 4),
    54: ("Outdoor Scrabble", "Word game taken outside for fresh air fun.", 4),
    55: ("Kite Flying", "Great for moderately windy days with some clouds.", 1),
    56: ("Fishing", "A relaxing activity for calm, cloudy days.", 1),
    57: ("Scavenger Hunt", "Organize an outdoor adventure game for groups in pleasant weather.", 10),
    58: ("Photography Walk", "Creative activity perfect for interesting weather conditions.", 1),
    59: ("Geocaching", "Modern treasure hunting using GPS technology.", 2),
    60: ("Board Games", "When weather isn't ideal, enjoy classic board games inside.", 4),
    61: ("Chess", "A quiet, strategic game you can play indoors or on covered patios.", 2),
    62: ("Card Games", "Classic entertainment perfect for any indoor gathering.", 4),
    63: ("Video Games", "Modern entertainment for when weather keeps you inside.", 4),
    64: ("Puzzle Solving", "Relaxing indoor activity perfect for rainy days.", 1),
    65: ("Table Tennis (Indoor)", "Fast-paced indoor sport for any weather.", 2),
    66: ("Bowling", "Classic indoor sport perfect for groups.", 6),
    67: ("Pool/Billiards", "Precision indoor game great for socializing.", 2),
    68: ("Darts", "Traditional pub game perfect for indoor gatherings.", 2),
    69: ("Indoor Rock Climbing", "Challenging sport that doesn't depend on weather.", 1),
    
    # New outdoor games (70-149)
    70: ("Archery", "Precision sport using bows and arrows", 1),
    71: ("Airsoft", "Tactical team shooting game with replica weapons", 12),
    72: ("Paintball", "Competitive shooting game with paint pellets", 10),
    73: ("Orienteering", "Navigation sport using maps and compasses", 2),
    74: ("Mountain Biking", "Cycling on rough terrain, best in dry conditions", 1),
    75: ("Trail Hiking", "Hiking on marked trails through nature", 2),
    76: ("Bird Watching", "Relaxing nature observation activity", 2),
    77: ("Outdoor Photography", "Creative photography in natural settings", 1),
    78: ("Stargazing", "Nighttime activity best in clear skies", 2),
    79: ("Gardening", "Productive outdoor activity for pleasant weather", 1),
    80: ("Outdoor Chess", "Large-scale chess played in parks", 2),
    81: ("Outdoor Yoga", "Yoga practice in natural surroundings", 1),
    82: ("Tai Chi in Park", "Slow martial arts movements in peaceful settings", 1),
    83: ("Outdoor Meditation", "Mindfulness practice in nature", 1),
    84: ("Fishing (Fly)", "Specialized fishing technique for rivers", 1),
    85: ("Fishing (Ice)", "Winter fishing activity on frozen lakes", 2),
    86: ("Fishing (Deep Sea)", "Ocean fishing adventure", 6),
    87: ("Kayaking", "Paddling sport for lakes and calm rivers", 1),
    88: ("Canoeing", "Traditional paddling activity", 2),
    89: ("Rafting", "Whitewater team adventure sport", 8),
    90: ("Sailing", "Wind-powered boating activity", 4),
    91: ("Windsurfing", "Combination of surfing and sailing", 1),
    92: ("Kite Surfing", "Extreme water sport using kite power", 1),
    93: ("Paragliding", "Recreational flying with parachute-like wings", 1),
    94: ("Hang Gliding", "Air sport using unpowered aircraft", 1),
    95: ("Hot Air Ballooning", "Leisurely aerial activity", 4),
    96: ("Zip Lining", "Thrilling activity sliding on cables", 1),
    97: ("Bungee Jumping", "Extreme sport involving jumping from height", 1),
    98: ("Rock Climbing (Outdoor)", "Natural rock face climbing", 2),
    99: ("Mountain Climbing", "Challenging ascent of mountains", 4),
    100: ("Caving", "Exploring underground cave systems", 4),
    
    # Indoor Sports (101-200)
    101: ("Indoor Soccer", "Soccer adapted for indoor courts", 10),
    102: ("Indoor Volleyball", "Volleyball played in gymnasiums", 12),
    103: ("Indoor Basketball", "Basketball played on indoor courts", 10),
    104: ("Indoor Rock Climbing", "Climbing on artificial walls", 1),
    105: ("Indoor Swimming", "Pool swimming regardless of weather", 1),
    106: ("Squash", "Fast-paced racket sport in enclosed court", 2),
    107: ("Racquetball", "High-energy indoor racket sport", 2),
    108: ("Handball (Indoor)", "Team sport played with hands", 14),
    109: ("Futsal", "Indoor variant of soccer", 10),
    110: ("Indoor Cycling", "Stationary bike workouts", 1),
    111: ("Aerobics", "Group fitness classes", 15),
    112: ("Zumba", "Dance-based fitness program", 20),
    113: ("Pilates", "Low-impact flexibility exercises", 1),
    114: ("Martial Arts", "Various combat sports training", 2),
    115: ("Boxing", "Combat sport with gloves", 2),
    116: ("Wrestling", "Grappling combat sport", 2),
    117: ("Fencing", "Sword-based combat sport", 2),
    118: ("Gymnastics", "Artistic physical exercises", 1),
    119: ("Trampolining", "Jumping sport on elastic surface", 1),
    120: ("Parkour (Indoor)", "Urban movement training indoors", 1),
    121: ("Dance Classes", "Various dance styles instruction", 10),
    122: ("Ballet", "Classical dance form", 1),
    123: ("Contemporary Dance", "Modern expressive dance", 1),
    124: ("Hip Hop Dance", "Street dance style", 1),
    125: ("Ballroom Dancing", "Partner dance styles", 2),
    126: ("Ice Skating (Indoor)", "Skating on artificial ice", 1),
    127: ("Curling", "Team sport on ice with stones", 8),
    128: ("Indoor Archery", "Archery practice inside", 1),
    129: ("Shooting Range", "Firearm or airgun practice", 1),
    130: ("Bowling (10-pin)", "Traditional bowling game", 6),
    131: ("Bowling (Duckpin)", "Variation with smaller balls", 6),
    132: ("Bowling (Candlepin)", "Northeastern US variation", 6),
    133: ("Billiards (8-ball)", "Popular cue sport", 2),
    134: ("Billiards (9-ball)", "Rotation pool game", 2),
    135: ("Billiards (Snooker)", "English cue sport", 2),
    136: ("Carrom", "Strike-and-pocket table game", 4),
    137: ("Air Hockey", "Puck game on air-cushioned table", 2),
    138: ("Foozball", "Table soccer game", 2),
    139: ("Darts (501)", "Traditional dart game", 2),
    140: ("Darts (Cricket)", "Scoring dart game", 2),
    141: ("Shuffleboard", "Puck-sliding game", 2),
    142: ("Table Shuffleboard", "Table version of shuffleboard", 2),
    143: ("Ping Pong (Table Tennis)", "Fast-paced racket sport", 2),
    144: ("Beer Pong", "Social drinking game", 4),
    145: ("Cornhole (Indoor)", "Bean bag toss game inside", 4),
    146: ("Giant Jenga (Indoor)", "Large block stacking game", 4),
    147: ("Escape Room", "Interactive puzzle experience", 6),
    148: ("Virtual Reality Games", "Immersive digital gaming", 1),
    149: ("Laser Tag", "Team shooting game with lasers", 12),
    150: ("Indoor Mini Golf", "Miniature golf inside", 4),
    151: ("Board Game Cafe", "Social board gaming venue", 4),
    152: ("Card Game Tournament", "Competitive card playing", 8),
    153: ("Chess Club", "Organized chess playing", 2),
    154: ("Mahjong", "Traditional tile-based game", 4),
    155: ("Go", "Ancient strategic board game", 2),
    156: ("Backgammon", "Classic board game with dice", 2),
    157: ("Scrabble", "Word-formation board game", 4),
    158: ("Monopoly", "Classic property trading game", 6),
    159: ("Poker Night", "Social card game event", 8),
    160: ("Bridge", "Trick-taking card game", 4),
    161: ("Dungeons & Dragons", "Fantasy role-playing game", 5),
    162: ("Warhammer", "Tabletop miniature wargame", 2),
    163: ("Magic: The Gathering", "Collectible card game", 2),
    164: ("Yu-Gi-Oh!", "Japanese collectible card game", 2),
    165: ("Pokémon TCG", "Trading card game based on Pokémon", 2),
    166: ("Jigsaw Puzzles", "Picture assembly puzzles", 1),
    167: ("Crossword Puzzles", "Word-based puzzles", 1),
    168: ("Sudoku", "Number placement puzzle", 1),
    169: ("Rubik's Cube", "3D combination puzzle", 1),
    170: ("Karaoke", "Singing along to music", 1),
    171: ("Bingo", "Number matching game", 1),
    172: ("Trivia Night", "Knowledge-based competition", 8),
    173: ("Charades", "Acting-based party game", 6),
    174: ("Pictionary", "Drawing-based guessing game", 4),
    175: ("Heads Up!", "Word guessing party game", 4),
    176: ("Twister", "Physical party game", 4),
    177: ("Jenga", "Block stacking game", 2),
    178: ("Uno", "Color and number matching card game", 4),
    179: ("Dominoes", "Tile-based matching game", 4),
    180: ("Checkers", "Classic board strategy game", 2),
    181: ("Connect Four", "Vertical strategy game", 2),
    182: ("Battleship", "Guessing board game", 2),
    183: ("Operation", "Skill-based board game", 2),
    184: ("Clue", "Mystery-solving board game", 6),
    185: ("Risk", "World domination strategy game", 6),
    186: ("Settlers of Catan", "Resource management game", 4),
    187: ("Ticket to Ride", "Train route building game", 5),
    188: ("Pandemic", "Cooperative board game", 4),
    189: ("Codenames", "Word association party game", 6),
    190: ("Cards Against Humanity", "Adult party game", 4),
    191: ("Exploding Kittens", "Strategic card game", 5),
    192: ("Jackbox Games", "Digital party game collection", 8),
    193: ("Video Game Tournament", "Competitive video gaming", 8),
    194: ("Retro Gaming Night", "Classic video game session", 4),
    195: ("VR Fitness", "Exercise through virtual reality", 1),
    196: ("Indoor Trampoline Park", "Jumping activities center", 1),
    197: ("Ninja Warrior Course", "Obstacle course training", 1),
    198: ("Indoor Skydiving", "Simulated freefall experience", 1),
    199: ("Axe Throwing", "Target throwing activity", 2),
    200: ("Escape Room", "Themed puzzle-solving challenge", 6),
    
    # Seasonal/Weather-Specific Games (201-250)
    201: ("Snowboarding", "Winter sport on snow-covered slopes", 1),
    202: ("Skiing (Alpine)", "Downhill snow sport", 1),
    203: ("Skiing (Cross-Country)", "Endurance snow sport", 1),
    204: ("Ice Hockey (Outdoor)", "Team sport on frozen surfaces", 12),
    205: ("Ice Skating (Outdoor)", "Skating on natural ice", 1),
    206: ("Snowshoeing", "Winter hiking with special footwear", 2),
    207: ("Sledding", "Recreational sliding on snow", 2),
    208: ("Tubing (Snow)", "Sliding on inner tubes", 2),
    209: ("Ice Fishing", "Fishing through holes in frozen water", 2),
    210: ("Winter Camping", "Camping in cold weather conditions", 4),
    211: ("Northern Lights Viewing", "Observing aurora borealis", 2),
    212: ("Dog Sledding", "Transportation using dog teams", 4),
    213: ("Curling (Outdoor)", "Team sport on natural ice", 8),
    214: ("Snow Fort Building", "Constructing structures from snow", 4),
    215: ("Snowball Fight", "Casual winter combat game", 6),
    216: ("Ice Sculpting", "Artistic carving of ice", 1),
    217: ("Polar Plunge", "Brief swimming in freezing water", 1),
    218: ("Hot Springs Soaking", "Relaxing in natural warm waters", 2),
    219: ("Beachcombing", "Searching beaches for interesting items", 1),
    220: ("Sandcastle Building", "Creative sand sculpture", 2),
    221: ("Sunbathing", "Relaxing in sunlight", 1),
    222: ("Tide Pool Exploring", "Examining coastal ecosystems", 2),
    223: ("Snorkeling", "Surface-level underwater exploration", 1),
    224: ("Scuba Diving", "Underwater diving with equipment", 2),
    225: ("Whale Watching", "Observing marine mammals", 6),
    226: ("Dolphin Spotting", "Viewing dolphins in their habitat", 4),
    227: ("Beach Yoga", "Yoga practice on sandy shores", 1),
    228: ("Beach Meditation", "Mindfulness by the ocean", 1),
    229: ("Beach Cleanup", "Environmental activity", 8),
    230: ("Coastal Hiking", "Walking along shorelines", 2),
    231: ("Cliff Jumping", "Jumping into water from heights", 1),
    232: ("Coasteering", "Combination of swimming and climbing", 4),
    233: ("Sea Kayaking", "Kayaking in ocean environments", 1),
    234: ("Stand-Up Paddleboarding (Ocean)", "SUP in sea waters", 1),
    235: ("Surf Fishing", "Fishing from ocean shores", 2),
    236: ("Beach Volleyball (Night)", "Evening beach sport", 4),
    237: ("Bonfire Gathering", "Social event around fire", 8),
    238: ("Stargazing (Beach)", "Night sky observation", 2),
    239: ("Moonlight Walk", "Evening stroll", 2),
    240: ("Night Photography", "Low-light photography", 1),
    241: ("Glow-in-the-Dark Games", "Luminous nighttime activities", 6),
    242: ("Flashlight Tag", "Nighttime version of tag", 8),
    243: ("Ghost Stories", "Spooky tale-telling", 6),
    244: ("Outdoor Movie Night", "Film screening under stars", 10),
    245: ("Meteor Shower Watching", "Observing celestial events", 2),
    246: ("Camping", "Overnight outdoor stays", 4),
    247: ("Glamping", "Luxury camping experience", 2),
    248: ("RV Road Trip", "Traveling with recreational vehicle", 6),
    249: ("Picnicking", "Outdoor meal experience", 4),
    250: ("Farmers Market Visit", "Shopping for local produce", 2)
} 

weather_conditions = [
    "Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm", "Snow", 
    "Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", 
    "Squall", "Tornado", "Hurricane", "Typhoon", "Blizzard",
    "Freezing Rain", "Sleet", "Heat Wave", "Cold Wave"
]


def generate_comprehensive_training_data():
    """Generate more diverse and comprehensive training scenarios"""
    training_scenarios = [
        # Perfect weather scenarios
        {"temp_range": (22, 28), "wind_range": (0, 8), "cloud_range": (0, 25), 
         "weather": "Clear", "games": [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 45, 46, 47, 48], "count": 25},
        
        # Hot sunny weather
        {"temp_range": (28, 40), "wind_range": (0, 12), "cloud_range": (0, 30), 
         "weather": "Clear", "games": [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 3, 21, 22], "count": 30},
        
        # Mild pleasant weather
        {"temp_range": (18, 25), "wind_range": (0, 10), "cloud_range": (0, 40), 
         "weather": "Clear", "games": [35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 57, 58, 59], "count": 25},
        
        # Cool but clear weather
        {"temp_range": (10, 18), "wind_range": (2, 12), "cloud_range": (0, 50), 
         "weather": "Clear", "games": [35, 36, 43, 56, 70, 73, 74, 75, 76, 77], "count": 20},
        
        # Windy but clear conditions
        {"temp_range": (15, 25), "wind_range": (15, 30), "cloud_range": (10, 60), 
         "weather": "Clear", "games": [55, 91, 92, 14, 17, 18, 49, 50], "count": 20},
        
        # Very windy conditions
        {"temp_range": (10, 25), "wind_range": (25, 40), "cloud_range": (20, 80), 
         "weather": "Clear", "games": [55, 60, 61, 62, 65, 66, 67, 68, 69], "count": 15},
        
        # Partly cloudy pleasant
        {"temp_range": (18, 26), "wind_range": (3, 12), "cloud_range": (30, 70), 
         "weather": "Clouds", "games": [2, 6, 7, 8, 9, 10, 11, 35, 36, 43, 56, 78], "count": 25},
        
        # Overcast but mild
        {"temp_range": (15, 22), "wind_range": (5, 15), "cloud_range": (70, 95), 
         "weather": "Clouds", "games": [49, 56, 58, 59, 77, 78, 35, 36, 61, 62], "count": 20},
        
        # Cold and cloudy
        {"temp_range": (5, 15), "wind_range": (5, 20), "cloud_range": (60, 100), 
         "weather": "Clouds", "games": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 49], "count": 25},
        
        # Light rain
        {"temp_range": (10, 20), "wind_range": (3, 15), "cloud_range": (80, 100), 
         "weather": "Drizzle", "games": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 104, 105], "count": 30},
        
        # Heavy rain
        {"temp_range": (8, 18), "wind_range": (8, 25), "cloud_range": (90, 100), 
         "weather": "Rain", "games": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 101, 102, 103], "count": 35},
        
        # Thunderstorm
        {"temp_range": (15, 25), "wind_range": (15, 35), "cloud_range": (85, 100), 
         "weather": "Thunderstorm", "games": [60, 61, 62, 63, 64, 147, 148, 149, 150], "count": 25},
        
        # Light snow
        {"temp_range": (-2, 5), "wind_range": (2, 15), "cloud_range": (70, 100), 
         "weather": "Snow", "games": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 214, 215], "count": 20},
        
        # Heavy snow
        {"temp_range": (-10, 2), "wind_range": (5, 25), "cloud_range": (80, 100), 
         "weather": "Snow", "games": [201, 202, 203, 206, 207, 208, 214, 215, 60, 61, 62], "count": 25},
        
        # Freezing conditions
        {"temp_range": (-15, 0), "wind_range": (0, 20), "cloud_range": (40, 90), 
         "weather": "Snow", "games": [201, 202, 203, 204, 205, 209, 210, 85], "count": 20},
        
        # Foggy/Misty conditions
        {"temp_range": (5, 20), "wind_range": (0, 8), "cloud_range": (60, 100), 
         "weather": "Mist", "games": [60, 61, 62, 104, 105, 56, 49], "count": 15},
        
        # Hot and humid
        {"temp_range": (28, 38), "wind_range": (0, 10), "cloud_range": (40, 80), 
         "weather": "Haze", "games": [25, 30, 31, 32, 33, 105, 60, 61, 62], "count": 20},
        
        # Extreme heat
        {"temp_range": (35, 45), "wind_range": (0, 15), "cloud_range": (0, 50), 
         "weather": "Clear", "games": [25, 30, 31, 105, 60, 61, 62, 63, 110], "count": 15},
        
        # Cold but clear
        {"temp_range": (0, 10), "wind_range": (0, 12), "cloud_range": (0, 40), 
         "weather": "Clear", "games": [85, 204, 205, 209, 60, 61, 62, 63, 64], "count": 18},
        
        # Moderate conditions - morning
        {"temp_range": (12, 20), "wind_range": (2, 8), "cloud_range": (10, 50), 
         "weather": "Clear", "games": [38, 81, 82, 83, 35, 43, 77, 58], "count": 20},
        
        # Evening conditions
        {"temp_range": (15, 25), "wind_range": (0, 10), "cloud_range": (0, 60), 
         "weather": "Clear", "games": [78, 238, 239, 240, 237, 244, 245], "count": 18},
        
        # Beach weather
        {"temp_range": (24, 32), "wind_range": (8, 18), "cloud_range": (0, 40), 
         "weather": "Clear", "games": [3, 21, 25, 31, 32, 33, 219, 220, 221, 222, 223], "count": 25},
        
        # Mountain weather
        {"temp_range": (8, 18), "wind_range": (10, 25), "cloud_range": (20, 70), 
         "weather": "Clouds", "games": [35, 74, 75, 98, 99, 73, 100], "count": 18},
        
        {"temp_range": (15, 28), "wind_range": (5, 15), "cloud_range": (30, 80), 
         "weather": "Clouds", "games": [40, 41, 42, 59, 77, 6, 49, 50], "count": 22}
    ]
    
    features = []
    labels = []
    
    for scenario in training_scenarios:
        for _ in range(scenario["count"]):
            temp = np.random.uniform(*scenario["temp_range"])
            wind = np.random.uniform(*scenario["wind_range"])
            clouds = np.random.uniform(*scenario["cloud_range"])
            weather = scenario["weather"]
            
            # Add some randomization to make model more robust
            temp += np.random.normal(0, 1)  # Small temperature variation
            wind += np.random.normal(0, 0.5)  # Small wind variation
            clouds += np.random.normal(0, 3)  # Small cloud variation
            
            # Ensure values stay within reasonable bounds
            temp = max(-20, min(50, temp))
            wind = max(0, min(50, wind))
            clouds = max(0, min(100, clouds))
            
            game = np.random.choice(scenario["games"])
            features.append([temp, wind, clouds, weather])
            labels.append(game)
    
    return features, labels

weather_features, game_labels = generate_comprehensive_training_data()
print(f"Generated {len(weather_features)} training samples")

le = LabelEncoder()
weather_main_list = [row[3] for row in weather_features]
weather_main_encoded = le.fit_transform(weather_main_list)

X_train = [[row[0], row[1], row[2], weather_main_encoded[i]] for i, row in enumerate(weather_features)]
y_train = game_labels

model = RandomForestClassifier(
    n_estimators=300, 
    random_state=42,
    max_depth=15,      
    min_samples_split=3,
    min_samples_leaf=2,
    max_features='sqrt'
)
model.fit(X_train, y_train)

def get_diverse_game_recommendations(temp, wind_speed, cloudiness, weather_main, num_recommendations=6):
    """Get diverse game recommendations with fallback logic"""
    
    # Convert input values to Python native types to avoid JSON serialization issues
    temp = float(temp)
    wind_speed = float(wind_speed)
    cloudiness = float(cloudiness)
    weather_main = str(weather_main)
    
    # Extreme weather fallbacks
    if weather_main in ["Rain", "Drizzle", "Thunderstorm"]:
        indoor_options = list(range(60, 200))
        selected = random.sample(indoor_options, min(num_recommendations, len(indoor_options)))
        return selected
    
    elif weather_main == "Snow" or temp < -5:
        winter_options = list(range(201, 218)) + list(range(60, 120))
        selected = random.sample(winter_options, min(num_recommendations, len(winter_options)))
        return selected
    
    elif temp > 35:
        hot_weather_options = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 105] + list(range(60, 90))
        selected = random.sample(hot_weather_options, min(num_recommendations, len(hot_weather_options)))
        return selected
    
    elif wind_speed > 30:
        low_wind_options = [55] + list(range(60, 120))
        selected = random.sample(low_wind_options, min(num_recommendations, len(low_wind_options)))
        return selected
    
    # Use ML model for normal conditions
    try:
        if weather_main not in le.classes_:
            weather_main = "Clear" if cloudiness < 50 else "Clouds"
        
        encoded_weather = le.transform([weather_main])[0]
        X_test = [[temp, wind_speed, cloudiness, encoded_weather]]
        
        probabilities = model.predict_proba(X_test)[0]
        classes = model.classes_
        
        prob_dict = {int(classes[i]): float(probabilities[i]) for i in range(len(classes))}
        
        sorted_games = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        
        top_candidates = [int(game_id) for game_id, _ in sorted_games[:num_recommendations*2]]
        
        final_selection = random.sample(top_candidates, min(num_recommendations, len(top_candidates)))
        
        # Ensure all game IDs are Python integers
        return [int(game_id) for game_id in final_selection]
        
    except Exception as e:
        print(f"Model prediction error: {e}")
        if temp > 25:
            return random.sample([25, 3, 0, 6, 38, 49, 21, 22, 32, 33], num_recommendations)
        elif temp > 15:
            return random.sample([2, 5, 6, 0, 45, 57, 35, 36, 43], num_recommendations)
        else:
            return random.sample([60, 61, 35, 36, 49, 58, 62, 63, 64], num_recommendations)

@app.route("api/recommend-game", methods=["POST"])
def recommend_game():
    try:
        data = request.json
        
        temp = float(data.get("main", {}).get("temp", 20))
        wind_speed = float(data.get("wind", {}).get("speed", 5))
        cloudiness = float(data.get("clouds", {}).get("all", 0))
        weather_main = str(data.get("weather", [{}])[0].get("main", "Clear"))
        
        recommended_game_ids = get_diverse_game_recommendations(
            temp, wind_speed, cloudiness, weather_main
        )
        
        recommendations = []
        for game_id in recommended_game_ids:
            if game_id in game_map:
                title, description, players = game_map[game_id]
                recommendations.append({
                    "id": int(game_id),  # Ensure it's Python int
                    "title": str(title),
                    "description": str(description),
                    "players": int(players)
                })
        
        return jsonify({
            "weather_summary": {
                "temperature": float(temp),
                "wind_speed": float(wind_speed),
                "cloudiness": float(cloudiness),
                "condition": str(weather_main)
            },
            "recommendations": recommendations,
            "total_options": int(len(recommendations))
        })
        
    except Exception as e:
        return jsonify({"error": f"Recommendation failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4000, host='0.0.0.0')