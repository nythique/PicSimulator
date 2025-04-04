#include <stdio.h>
#include <stdbool.h>
#include <SDL.h>
#include <SDL_ttf.h>

#define BLUE "\033[34m"
#define RED "\033[31m"
#define GREEN "\033[32m"
#define YELLOW "\033[33m"
#define NOR "\033[0m"
#define RESET "\033[0m"

int main(int argc, char *argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf(RED"[ERREUR] Initialisation de SDL_Init échoué: %s.\n"RESET, SDL_GetError());
        return 1;
    }// Init de SDL et SDL_ttf (Retourne une erreur pour chaque si erreur)
    if (TTF_Init() != 0) {
        printf(RED"[ERREUR] Initialisation de TTF_Init échoué: %s."RESET, TTF_GetError());
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow("Visualiser PicSimulator", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 1000, 500, SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE);
    if (!window) {
        printf(RED"[ERREUR] Creation de la fenetre échoué: %s.\n"RESET, SDL_GetError());
        SDL_Quit();
        return 1;
    }// Creation de la fenetre !

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        printf(RED"[ERREUR] Creation du moteur de rendu échoué: %s.\n"RESET, SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }// Creation du moteur de rendu !

    TTF_Font * font = TTF_OpenFont("arial.ttf", 24);
    if (!font) {
        printf(YELLOW"[ERREUR] Chargement de la police échoué: %s.\n"RESET, TTF_GetError());
        return 1;
    }

    bool running = true; // Event d'ouverture de la fenetre est vraie (si l'executable est lançé)!
    SDL_Event event; //Creation d'une variabble d'event !

    while (running) { // Boucle primcipale
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) { // SI, Il y a clic sur le bouton de fermeture (X),
                running = false; // Fermerture de la fenetre si vrai!
            }
        }
        
        
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Fond noir (Config Background)
        SDL_RenderClear(renderer); // Effacer l'écran !
        SDL_SetRenderDrawColor(renderer, 255,0, 0, 255); // Couleur d'un carré ( Config blanc)
        SDL_Rect carre = {300, 250, 100, 100}; // x(largeur) et y(hauteur), Config de la dimension !
        SDL_RenderDrawRect(renderer, &carre); // Dessiner juste les contours !

        //{DESSINER DU TEXTE}
        // Définir la couleur du texte (blanc)
        SDL_Color color = {255, 255, 255};
        // Créer une surface avec le texte
        SDL_Surface *surface = TTF_RenderText_Solid(font, "Options1", color);
        // Convertir en texture
        SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);
        // Définir la position du texte
        SDL_Rect dest = {50, 50, surface->w, surface->h};
        // Afficher le texte
        SDL_RenderCopy(renderer, texture, NULL, &dest);
        // Libérer la mémoire temporaire
        SDL_FreeSurface(surface);
        SDL_DestroyTexture(texture);


        SDL_RenderPresent(renderer); // Affiche le rendu !

        SDL_Delay(16); // Pour éviter d'utiliser trop de ressources CPU (~60 FPS)
    }
     // {Nettoyage}
    TTF_CloseFont(font); // Fermerture du font !
    SDL_DestroyRenderer(renderer); // Destruction des fond !
    SDL_DestroyWindow(window); // Destruction de la fenetre !
    TTF_Quit(); // Exit du font !
    SDL_Quit(); // Exit

    return 0;
}



