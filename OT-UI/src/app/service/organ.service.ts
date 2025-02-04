import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OrganService {
  private apiUrl = 'https://localhost:7271/api/Organ/match';  // .NET API URL

  constructor(private http: HttpClient) {}

  getBestDonor(recipient: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, recipient);
  }
}
