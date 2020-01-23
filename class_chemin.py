config = {
    'startpath': r'/Users/Y_KADRI/Desktop/Image_save',

    'fichier_anonymisation': r'/Users/Y_KADRI/Desktop/Copie_AnomymisationBioprostic.xlsx',

}


class Config:
    def __init__(self, param):
        self.startpath = param['startpath']
        self.fichier_anonymisation = param['fichier_anonymisation']

    def __repr__(self):
        return "Ca fontionne !!"






