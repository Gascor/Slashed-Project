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
    video.addEventListener('canplay', () => {
      video.play();
    });
  }
}