import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface News {
  id: number;
  title: string;
  description: string;
  image_url: string;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiUrl = 'https://apigw-slashedproject.fr/news';

  constructor(private http: HttpClient) { }

  getNews(): Observable<News[]> {
    return this.http.get<News[]>(this.apiUrl);
  }
}