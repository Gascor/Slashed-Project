import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { VideoBackgroundComponent } from './video-background.component'; // Chemin corrigé

@NgModule({
  declarations: [
    AppComponent,
    VideoBackgroundComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }