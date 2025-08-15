import pygame

class InitPyGame:
    def __init__(self, screenSize, gameName="New Game", fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption(gameName)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.deltaTime = 0
        self.keys = None
        self.events = []
        self.keyPressed = set()
        self.keyReleased = set()
        self.mouseButtonDown = set()
        self.start_func = None
        self.eventHandlers = {}
        self.customEvents = {}

    def onEvent(self, name, func, delay=None):
        eventType = pygame.USEREVENT + len(self.customEvents)
        self.customEvents[name] = eventType
        self.eventHandlers[name] = func

        if delay != None:
            pygame.time.set_timer(eventType, delay)

    def convertDelta(self, value):
        """Converts a speed in pixels/sec to pixels/frame."""
        return value * self.deltaTime

    def isKeyPressed(self, key):
        """Returns True if key was pressed this frame (KEYDOWN)."""
        return key in self.keyPressed

    def isKeyReleased(self, key):
        """Returns True if key was released this frame (KEYUP)."""
        return key in self.keyReleased

    """
    Button is either
    1: left click
    2: middle click
    3: right click
    4: scroll wheel up
    5: scroll wheel down
    """
    def isMouseButtonDown(self, button:int):
        """Returns True if button was pressed this frame (MOUSEBUTTONDOWN)."""
        return button in self.mouseButtonDown
    
    def onStart(self, func):
        self.start_func = func

    def gameloop(self, update):

        if self.start_func:
            self.start_func(self)

        while True:
            # Clear one-frame key press/release trackers
            self.keyPressed.clear()
            self.keyReleased.clear()
            self.mouseButtonDown.clear()

            
            # Get events for this frame
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyReleased.add(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonDown.add(event.button)

                for name, eventType in self.customEvents.items():
                    if event.type == eventType:
                        self.eventHandlers[name](self)
                        
            # Get current keys held
            self.keys = pygame.key.get_pressed()

            # Calculate delta time
            self.deltaTime = self.clock.tick(self.fps) / 1000.0

            # Call update function
            update(self, self.screen, self.keys, self.events)

            # Refresh display
            pygame.display.flip()
