import os
from random import choice
from datetime import datetime
import pandas as pd
import time
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.cloud import storage
import pickle
from dotenv import load_dotenv

load_dotenv()

# Define the credentials scope required for uploading videos
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Define the credentials JSON file path (downloaded from the Google Cloud Console)
CREDENTIALS_FILE = os.getenv('YOUTUBE_OAUTH')

# Initial credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_STORAGE_KEY')

# Generates the tags and caption for the video
def caption_gen():
    description = """

    Downloading and using this beat is subject to terms and conditions below:
     1. Dont make a bad song with it
     2. Dont break rule #1
     3. If you upload the song, include my channel "Gablo Ficazzo" in the tags or description so i can find it.
        As of now i do not have social media, so that is the only way i will be able to see the song.

    """
    tags = ["beats",
            "typebeat",
            ]
    artists = [    
        'Lil Nas X',
        'Roddy Ricch',
        'DaBaby',
        'Megan Thee Stallion',
        'Pop Smoke',
        'Jack Harlow',
        'Lil Baby',
        'NLE Choppa',
        'Mulatto',
        'Flo Milli',
        'Polo G',
        'Lil Tjay',
        'Saweetie',
        'Cordae',
        'JID',
        'YBN Cordae',
        'Lil Uzi Vert',
        'Smokepurpp',
        'Trippie Redd',
        'Ski Mask the Slump God',
        'XXXTentacion',
        'Lil Peep',
        '6ix9ine',
        'YBN Nahmir',
        'Playboi Carti',
        'Drake',
        'Travis Scott',
        'Post Malone',
        'Kanye West',
        'Lil Wayne',
        'Migos',
        'Future',
        'A$AP Rocky',
        'Tyler, The Creator'
        ]
    for x in range(3):
        artist = choice(artists)
        if artists not in tags:
            tags.append(artist)
        else:
            continue

    return (tags, description)

# Creates info dict for db_update
def info_dict_gen(audiopath):
    # Variables for beat titles
    gpt_titles = [
        'Aeon',
        'Aloft',
        'Amulet',
        'Anima',
        'Aphelion',
        'Astral',
        'Atrium',
        'Aurum',
        'Avant',
        'Axion',
        'Azimuth',
        'Beryl',
        'Baryon',
        'Basilisk',
        'Bastion',
        'Belladonna',
        'Bijou',
        'Brio',
        'Brume',
        'Caelum',
        'Caldera',
        'Candescence',
        'Canorous',
        'Capriccio',
        'Caprice',
        'Carillon',
        'Carnelian',
        'Celesta',
        'Cerulean',
        'Chanticleer',
        'Chiaroscuro',
        'Chrysalis',
        'Cinnabar',
        'Citrine',
        'Cloudburst',
        'Cognac',
        'Concordance',
        'Copse',
        'Crepuscular',
        'Crimson',
        'Cronus',
        'Crysalis',
        'Crystal',
        'Cynosure',
        'Dalliance',
        'Damsel',
        'Dante',
        'Dazzle',
        'Debonair',
        'Decadent',
        'Demure',
        'Denouement',
        'Desideratum',
        'Destrier',
        'Diadem',
        'Diamantine',
        'Diffuse',
        'Dissonance',
        'Divination',
        'Divisio',
        'Dolce',
        'Dolorous',
        'Douceur',
        'Echelon',
        'Eclat',
        'Effervescence',
        'Efflorescence',
        'Elegance',
        'Elixir',
        'Elysian',
        'Embark',
        'Embroider',
        'Emollient',
        'Empyrean',
        'Endeavour',
        'Enigma',
        'Ennui',
        'Ephemera',
        'Epiphany',
        'Eponymous',
        'Equanimity',
        'Erelong',
        'Erstwhile',
        'Esprit',
        'Ethereal',
        'Eudaimonia',
        'Euphony',
        'Eurydice',
        'Eutony',
        'Evince',
        'Exalt',
        'Exigency',
        'Expatiate',
        'Expiate',
        'Exquisite',
        'Extol',
        'Facile',
        'Fallow',
        'Fandango',
        'Fascicle',
        'Fawn',
        'Fealty',
        'Felicitous',
        'Ferrous',
        'Fervent',
        'Festoon',
        'Fidelitous',
        'Flamboyant',
        'Flaxen',
        'Fleur-de-lis',
        'Flourish',
        'Folly',
        'Foppish',
        'Forbearance',
        'Fracas',
        'Fulgent',
        'Fulsome',
        'Furtive',
        'Gallant',
        'Gambol',
        'Gamine',
        'Gargantuan',
        'Gelid',
        'Genial',
        'Gilt',
        'Gleam',
        'Glimmer',
        'Glisten',
        'Glitter',
        'Gloaming',
        'Glorious',
        'Gossamer',
        'Grandiloquent',
        'Gregarious',
        'Grisaille',
        'Gumption',
        'Halcyon',
        'Harbinger',
        'Hearth',
        'Heliocentric',
        'Hemisphere',
        'Hemistich',
        'Heritage',
        'Heterogeneous',
        'Hibernal',
        'Hillside',
        'Hypostasis',
        'Iconoclast',
        'Idiosyncrasy',
        'Ignite',
        'Illusory',
        'Imbue',
        'Immaculate',
        'Immerse',
        'Imminent',
        'Immutable',
        'Impassioned',
        'Imperative',
        'Imperial',
        'Impervious',
        'Impetuous',
        'Impinge',
        'Implore',
        'Impromptu',
        'Impulse',
        'Inception',
        'Inchoate',
        'Incipient',
        'Indelible',
        'Indomitable',
        'Indulge',
        'Ineffable',
        'Inertia',
        'Inexorable',
        'Infallible',
        'Inglenook',
        'Ingenuity',
        'Inimitable',
        'Iniquity',
        'Innate',
        'Inscribe',
        'Insidious',
        'Insipid',
        'Insouciant',
        'Insurgence',
        'Interlocution',
        'Introspection',
        'Intrinsic',
        'Intrepid',
        'Inure',
        'Invocation',
        'Iridescent',
        'Irrepressible',
        'Jabberwock',
        'Jacinth',
        'Jaunty',
        'Jocund',
        'Juxtapose',
        'Kaleidoscope',
        'Ken',
        'Kindred',
        'Kinetic',
        'Kith',
        'Knell',
        'Kudos',
        'Labyrinthine',
        'Lachrymose',
        'Laguna',
        'Lambent',
        'Languor',
        'Largesse',
        'Lassitude',
        'Lavender',
        'Leitmotif',
        'Lepidoptera',
        'Lethargy',
        'Leviathan',
        'Liberate',
        'Limpid',
        'Lissome',
        'Lithe',
        'Liturgy',
        'Loquacious',
        'Luminary',
        'Lustrous',
        'Lyricism',
        'Macerate',
        'Maelstrom',
        'Magisterial',
        'Magnanimous',
        'Magnificence',
        'Majestic',
        'Malfeasance',
        'Malinger',
        'Malleable',
        'Mammoth',
        'Mandala',
        'Manifest',
        'Manifold',
        'Mantra',
        'Mantle',
        'Marquetry',
        'Martyrdom',
        'Masquerade',
        'Mastery',
        'Mausoleum',
        'Meadow',
        'Melancholy',
        'Meliorate',
        'Mellifluous',
        'Menagerie',
        'Mendacity',
        'Nacreous',
        'Nebulous',
        'Nefarious',
        'Neoteric',
        'Nescient',
        'Niveous',
        'Nocturne',
        'Oblivion',
        'Odyssey',
        'Omnipotent',
        'Onomatopoeia',
        'Opulence',
        'Oracular',
        'Oscillate',
        'Ossuary',
        'Ostentatious',
        'Overture',
        'Pallid',
        'Panacea',
        'Panoply',
        'Paradigm',
        'Paragon',
        'Parsimonious',
        'Pathos',
        'Pedagogy',
        'Pellucid',
        'Penumbra',
        'Perfidious',
        'Peripatetic',
        'Perpetuity',
        'Perspicacious',
        'Petrichor',
        'Philistine',
        'Phlegmatic',
        'Phosphorescent',
        'Picayune',
        'Plethora',
        'Polymath',
        'Ponderous',
        'Portentous',
        'Precipice',
        'Precursor',
        'Preeminence',
        'Prescience',
        'Primordial',
        'Prodigious',
        'Propinquity',
        'Protean',
        'Puerile',
        'Pulchritude',
        'Punctilious',
        'Pyrrhic',
        'Quaint',
        'Qualia',
        'Quantum',
        'Quell',
        'Querulous',
        'Quintessential',
        'Quixotic',
        'Raconteur',
        'Rancorous',
        'Rapacious',
        'Ratiocination',
        'Ravishing',
        'Rebarbative',
        'Recalcitrant',
        'Redolent',
        'Refulgent',
        'Rejoinder',
        'Relinquish',
        'Reminiscence',
        'Remonstrate',
        'Renascence',
        'Repertoire',
        'Repose',
        'Requiem',
        'Resplendent',
        'Reticent',
        'Reverie',
        'Rhapsodize',
        'Risible',
        'Riveting',
        'Robust',
        'Rococo',
        'Rubicon',
        'Rudimentary',
        'Ruminant',
        'Saccharine',
        'Sacrosanct',
        'Salubrious',
        'Sanguine',
        'Sapient',
        'Sardonic',
        'Satori',
        'Saturnine',
        'Scintilla',
        'Scintillating',
        'Sempiternal',
        'Serenade',
        'Serendipity',
        'Serene',
        'Shibboleth',
        'Shimmer',
        'Sibilant',
        'Sibylline',
        'Sidereal',
        'Siesta',
        'Simulacrum',
        'Sinecure',
        'Sinewy',
        'Singular',
        'Siren',
        'Sisyphean',
        'Skeptic',
        'Sleight',
        'Sobriquet',
        'Solecism',
        'Somnambulist',
        'Somnolent',
        'Soporific',
        'Soulful',
        'Spartan',
        'Specious',
        'Spurious',
        'Squander',
        'Staccato',
        'Stalwart',
        'Stentorian',
        'Sublime',
        'Subterfuge',
        'Succulent',
        'Suffuse',
        'Surreptitious',
        'Susurrous',
        'Sycophant',
        'Synchronicity',
        'Syzygy',
        'Taciturn',
        'Talisman',
        'Tangential',
        'Tantalize',
        'Tarnish',
        'Tenebrous',
        'Tenet',
        'Tenuous',
        'Terpsichorean',
        'Theurgy',
        'Threnody',
        'Titillate',
        'Toady',
        'Torpid',
        'Torrid',
        'Tortuous',
        'Traduce',
        'Tranquil',
        'Transcendent',
        'Transitory',
        'Tremulous',
        'Trepidation',
        'Tryst',
        'Tumultuous',
        'Turpitude',
        'Ubiquitous',
        'Umbrage',
        'Unassailable',
        'Unctuous',
        'Undulate',
        'Unfetter',
        'Unilateral',
        'Unmitigated',
        'Unremitting',
        'Unscrupulous',
        'Untoward',
        'Unwonted',
        'Upbraid',
        'Uproarious',
        'Usurp',
        'Utopia',
        'Vacuous',
        'Valediction',
        'Venerable',
        'Veracity',
        'Vestige',
        'Vicarious',
        'Vicissitude',
        'Vignette',
        'Vilify',
        'Vindictive',
        'Virtuoso',
        'Virulent',
        'Visceral',
        'Viscid',
        'Vitiate',
        'Vivacious',
        'Vociferous',
        'Voracious',
        'Welter',
        'Whimsical',
        'Winnow',
        'Wistful',
        'Wraith',
        'Xanadu',
        'Xenophobia',
        'Xylograph',
        'Yammer',
        'Yearning',
        'Yoke',
        'Yonder',
        'Zealot',
        'Zenith',
        'Zephyr',
        'Zestful',
        'Zigzag',
        'Zodiac',
        'Zoetic'
        ]
    title = choice(gpt_titles)
    code = ""
    for x in range(4):
        num = choice([0,1,2,3,4,5,6,7,8,9])
        code += str(num)

    info_dict = {}
    info_dict['ab_code'] = code
    info_dict['title'] = title
    info_dict['beat_name'] = audiopath.split("/")[-1]
    info_dict['link'] = ''
    info_dict['date_uploaded'] = datetime.today().date()
    info_dict['viewstodate'] = 0

    return info_dict

# General DB Update
def db_update(info_dict):
    # Accesses the previous database and appends new info from scrapes
    # Accepts: 
        # info: list of info from desired scrape
        # path: path to the current database
    # Returns:
        # None

    try:
        # Open storage client and download the database
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('autobeats-database')
        blob = bucket.blob('autobeats-dataframe.csv')
        blob.download_to_filename('autobeats-dataframe.csv')

        # Apending database info
        old_df = pd.read_csv(blob.name, index_col=0)
        apppendable = pd.DataFrame(info_dict, index=[0])
        new_df = pd.concat([old_df, apppendable], ignore_index=True)
        new_df.to_csv(blob.name, mode='w')
        print("Data appended successfully.")

        # Uploading database info
        blob.upload_from_filename("autobeats-dataframe.csv")
        print("Data uploaded to GCS successfully.")
        storage_client.close()
    
    except:
        apppendable = pd.DataFrame(info_dict, index=[0])
        storage_client = storage.Client()
        apppendable.to_csv(f"{datetime.today().date()}_appendable.csv")
        bucket = storage_client.get_bucket('autobeats-database')
        blob = bucket.blob(f"{datetime.today().date()}_appendable.csv")
        blob.upload_from_filename("autobeats-dataframe.csv")
        print("Incomplete information, please review appendable.")
        storage_client.close()

    return

# Downloads bg audio from gcs
def gcs_audio_downloader():
    """Pulls a random bg_video from the desired bucket"""

    # GCS Bucket Name where audio files are stored from .env
    bucket_name = os.getenv('GCS_BUCKET_NAME')

    # Note: Client.list_blobs requires at least package version 1.17.0.
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    # Note: The call returns a response only when the iterator is consumed.
    blob_list = [x.name for x in blobs]
    video = choice(blob_list)
    blob = bucket.get_blob(video)
    output_path = video.replace(" ", "_").replace("(", "").replace(")", "")
    blob.download_to_filename(output_path)

    storage_client.close()          # Closes client

    return output_path

# Compiles video and audio
def videocompiler(audiopath):

    # Path to background video from .env
    bg_video_path = os.getenv('BACKGROUND_VIDEO_PATH')  

    bgvideo = bg_video_path
    outputpath = f"{datetime.today().date()}-output.mp4"
    os.system(f"ffmpeg -i {bgvideo} -i {audiopath} -shortest -c copy -map 0:v:0 -map 1:a:0 {outputpath}")
    return outputpath

# Authenticates oauth acces, does not need to be called as it is already called in upload_video function
def authenticate():
    """
    Create and return an authenticated API client for the YouTube API v3.
    """
    # Path to token.pickle file
    pickle_token = os.getenv('TOKEN_PICKLE')   

    # Load the credentials from the file
    credentials = None
    if os.path.exists(pickle_token):
        with open(pickle_token, 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    # Create an authenticated API client
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

# Uploads final beat to youtube
def upload_video(video_file, video_title, video_description, video_tags, video_category_id):
    """
    Upload the specified video file to YouTube.
    """
    youtube = authenticate()

    channel_id = os.getenv('YOUTUBE_CHANNEL_ID')

    try:
        # Create a new video resource
        video = dict(
            snippet=dict(
                title=video_title,
                description=video_description,
                tags=video_tags,
                categoryId=video_category_id,
                channelId=channel_id
            ),
            status=dict(
                privacyStatus='public'
            )
        )

        # Upload the video file
        media = MediaFileUpload(video_file)
        request = youtube.videos().insert(
            part='snippet,status',
            body=video,
            media_body=media,
            notifySubscribers=False
        )
        response = request.execute()

        print(f"\nVideo id '{response['id']}' was successfully uploaded.")
        return f"https://www.youtube.com/watch?v={response['id']}"

    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred: {error.content}")
        return None

# Deletes all local files
def file_delete(audiopath, videopath):

    try:
        if os.path.exists(audiopath):
            os.remove(audiopath)
        if os.path.exists(videopath):
            os.remove(videopath)
        print("\nAll local files deleted.")

    except Exception as e:
        print(e)

    return

# Final Function Call
def AutoBeats():

    error_count = 0
    operation = True
    
    while operation == True:
        try:
            audiopath = gcs_audio_downloader()
            info_dict = info_dict_gen(audiopath=audiopath)
            title = info_dict['title']
            code = info_dict['ab_code']
            tags, description = caption_gen()
            videopath = videocompiler(audiopath)
            time.sleep(10)
            yt_link = upload_video(video_file=videopath, 
                                   video_title=f"""[FREE] "{title}" #Instrumental {code}""",
                                   video_description=description,
                                   video_tags=tags,
                                   video_category_id='10'
                                   )
            info_dict['link'] = yt_link
            db_update(info_dict)
            file_delete(audiopath, videopath)
            hours = 24
            for x in range(hours):
                print(f"Sleeping for {hours} more hours until a new video is made.")
                hours -= 1
                time.sleep(3600)

        except Exception as e:
            #error_count+=1
            print(e)
            file_delete(audiopath, videopath)
            if error_count > 3:
                operation=False
            else:
                continue

AutoBeats()
