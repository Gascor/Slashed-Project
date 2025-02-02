import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { VideoBackgroundComponent } from './assets/video-background.component'; // Adjust path if necessary

@NgModule({
  declarations: [
    AppComponent,
    VideoBackgroundComponent // Make sure it is listed here
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
