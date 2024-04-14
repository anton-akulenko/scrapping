from classes.singleton import Singleton


class Config(metaclass=Singleton):
    """Class for store all project settings."""

    URLS_24HEURES: list
    URLS_BREAKINGLATEST: list
    URLS_CHISWICKCALENDAR: list
    URLS_CORRIERE: list

    def __init__(self) -> None:
        """Load settings from file."""
        self.URLS_24HEURES = [
            "https://www.24heures.ch/football-le-lausanne-sport-se-rapproche-du-maintien-347973444223",
            "https://www.24heures.ch/guerre-en-ukraine-loffensive-de-larmee-russe-sintensifie-173690705771",
            "https://www.24heures.ch/le-sommet-pour-la-paix-en-ukraine-aura-lieu-au-buergenstock-705217304528",
            "https://www.24heures.ch/video-retour-sur-lhistoire-du-lausanne-hockey-club-100437814509",
        ]
        self.URLS_BREAKINGLATEST = [
            "https://www.breakinglatest.news/news/what-to-do-if-i-owe-the-irs-how-to-avoid-fines-for-"
            "not-paying-taxes-to-the-irs-univision-23-dallas-ft-worth-kuvn-univision-23-dallas/",
            "https://www.breakinglatest.news/news/a-center-to-learn-stories-of-coffee-growing-women-"
            "and-drink-a-good-coffee/",
            "https://www.breakinglatest.news/entertainment/popular-games-one-of-the-unfulfilled-"
            "promises-of-paris-2024/",
            "https://www.breakinglatest.news/world/shakira-set-coachella-on-fire-and-released-news/",
        ]

        self.URLS_CHISWICKCALENDAR = [
            "https://chiswickcalendar.co.uk/who-are-the-2024-candidates-for-the-south-west-london-"
            "seat-on-the-london-assembly/",
            "https://chiswickcalendar.co.uk/the-government-inspector-st-michaels-players/",
            "https://chiswickcalendar.co.uk/cache-of-paintings-of-chiswick-found-painted-by-once-"
            "celebrated-artist-heather-jenkins/",
            "https://chiswickcalendar.co.uk/train-derailment-in-west-ealing/",
        ]
        self.URLS_CORRIERE = [
            "https://www.corriere.it/esteri/24_aprile_14/rappresaglia-iran-incursione-risultati-modesti-show-forza-"
            "69681080-fa3f-11ee-ba6a-99e730c8c30b.shtml",
            "https://milano.corriere.it/notizie/cronaca/24_aprile_14/don-gianfranco-macor-esorcista-il-demonio-e-"
            "intelligente-chiunque-comandi-gli-interessa-e-milano-e-una-citta-di-potere-97e740f0-dd4e-"
            "491f-bf2b-4f1c4c58bxlk.shtml",
            "https://www.corriere.it/tecnologia/24_aprile_14/una-tesla-con-la-guida-autonoma-ha-portato-in-"
            "ospedale-un-uomo-colpito-da-crisi-iperglicemica-e-infarto-ba339b52-f6eb-4777-8015-52dd6a94bxlk.shtml",
            "https://www.corriere.it/salute/24_aprile_13/nostalgia-perche-si-prova-e-a-che-cosa-serve-"
            "f6696df6-47ef-4423-9b16-34a6e3da3xlk.shtml",
        ]
        self.INEWS_BASE = "https://inews.co.uk/category/news"
        self.SVT_BASE = "https://svt.se"
        self.RTP_BASE = "https://rtp.pt/noticias/"
        self.RTBF_BASE = "https://www.rtbf.be/en-continu/"


CONFIG = Config()
