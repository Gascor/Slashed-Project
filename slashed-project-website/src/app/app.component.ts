import { Component } from '@angular/core';
import { VideoBackgroundComponent } from './video-background.component'; // Chemin corrigé

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [VideoBackgroundComponent] // Ajoutez cette ligne
})
export class AppComponent {
  title = 'Slashed Project';
}