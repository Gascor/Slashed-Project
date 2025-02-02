import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { VideoBackgroundComponent } from './video-background/video-background.component'; // Chemin corrigé

@NgModule({
  imports: [
    BrowserModule,
    AppComponent,
    VideoBackgroundComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }