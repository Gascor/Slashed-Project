import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { VideoBackgroundComponent } from './video-background/video-background.component'; // Adjust the path as necessary

@NgModule({
  declarations: [
    AppComponent,
    VideoBackgroundComponent  // Make sure this is included
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
