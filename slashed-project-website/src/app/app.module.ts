import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';

@NgModule({
  imports: [BrowserModule, AppComponent],  // Importer au lieu de déclarer
  bootstrap: [AppComponent]
})
export class AppModule {}
