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
        // Réessayer de jouer la vidéo après un court délai
        setTimeout(tryPlayVideo, 1000);
      });
    };

    // Essayer de jouer la vidéo immédiatement
    tryPlayVideo();
  }
}