import time, os, pickle, requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from init_photo import service
from kivy.core.clipboard import Clipboard

Builder.load_file('configuration.kv')

def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png')):
    """
    Get the latest image file in the given directory
    """
    # get filepaths of all files and dirs in the given dir
    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    # filter out directories, no-extension, and wrong extension files
    valid_files = [f for f in valid_files if '.' in f and \
        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

    if not valid_files:
        raise ValueError("No valid images in %s" % dirpath)

    return max(valid_files, key=os.path.getmtime)

def upload_image(image_path, upload_file_name, token):
    '''
    This function uploads image taken from your camera, to Google Photos account:
    image_path: location where image is saved
    upload_file_name: name used for uploading to photos.google.com
    token: an authentification token
    '''
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'

    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw',
        'X-Goog-File-Name': upload_file_name
    }

    img = open(image_path, 'rb').read()
    response = requests.post(upload_url, data=img, headers=headers)
    print('\nUpload token: {0}'.format(response.content.decode('utf-8')))
    return response

class CameraScreen(Screen):
    def start(self):
        '''Starts camera and changes Button text'''
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        '''Stops camera and changes Button text'''
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        '''Creates a filename with current time and captures
        and saves a photo image under that filename'''
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.path = f'./captures/{current_time}-selfie.png'
        self.ids.camera.export_to_png(self.path)
        print(f'File saved in {self.path}')
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.path



class ImageScreen(Screen):

    def create_sharable_link(self):
        '''
        Creates a sharable link copied to clipboard. For using that link, use CTRL+V into a browser to view the
        image or refresh the page (www.photos.google.com)
        '''
        image_dir = os.path.join(os.getcwd(), 'captures')
        token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))

        tokens = []

        image1 = os.path.join(image_dir, get_latest_image(image_dir, 'png'))
        response = upload_image(image1, 'Selfie 1st', token)
        print(response)
        tokens.append(response.content.decode('utf-8'))
        new_media_items = [{'simpleMediaItem': {'uploadToken': tok}} for tok in tokens]

        request_body = {
            'newMediaItems': new_media_items
        }

        self.photo = service.mediaItems().batchCreate(body=request_body).execute()
        self.link = self.photo['newMediaItemResults'][0]['mediaItem']['productUrl']
        self.ids.text_link.text = 'Link copied'
        Clipboard.copy(self.link)
        print(self.link)

    def back(self):
        '''
        Deletes the latest photo captured and returns the user to Camera Screen.
        '''
        self.manager.current = 'camera_screen'
        self.image_dir = os.path.join(os.getcwd(), 'captures')
        os.remove(get_latest_image(self.image_dir, 'png'))


class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

app = MainApp()
app.run()

response = service.albums().list(
    pageSize=50,
    excludeNonAppCreatedData=False
).execute()

lstAlbums = response.get('albums')
nextPageToken = response.get('nextPageToken')