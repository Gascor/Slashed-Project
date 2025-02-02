import { Component, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-video-background',
  templateUrl: './video-background.component.html',
  styleUrls: ['./video-background.component.css'],
  standalone: true
})
export class VideoBackgroundComponent implements AfterViewInit {
  ngAfterViewInit() {
    const video = document.getElementById('video-background') as HTMLVideoElement;

    const tryPlayVideo = () => {
      video.play().catch(error => {
        console.error('Erreur lors de la lecture de la vidéo:', error);
      });
    };

    // Essayer de jouer la vidéo immédiatement
    tryPlayVideo();

    // Ajouter un écouteur d'événements pour détecter les mouvements de la souris
    document.addEventListener('mousemove', () => {
      tryPlayVideo();
    });
    document.addEventListener('click', () => {
      tryPlayVideo();
    });

    document.addEventListener('keydown', () => {
      tryPlayVideo();
    });
  }
}