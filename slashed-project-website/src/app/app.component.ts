import { Component } from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { VideoBackgroundComponent } from './video-background/video-background.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [HeaderComponent, VideoBackgroundComponent]
})
export class AppComponent {
  title = 'Slashed Project';
}