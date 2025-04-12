<<<<<<< HEAD
// src/app/services/evaluation.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
=======
import { Injectable } from '@angular/core';
>>>>>>> a5f00270d44e6bbdd13c6804586b07cb4aa4df06

@Injectable({
  providedIn: 'root'
})
<<<<<<< HEAD
export class EvaluationService {

  private baseUrl = 'http://localhost:5000/api'; // Ton URL backend

  constructor(private http: HttpClient) { }

  // Méthode pour récupérer les évaluations
  getEvaluations(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/evaluations`);
  }

  // Méthode pour dupliquer un test
  duplicateTest(oldTestId: number, payload: any): Observable<any> {
    // payload peut contenir { nom, description, groupes_ids, ... }
    return this.http.post(`${this.baseUrl}/tests/duplicate/${oldTestId}`, payload);
  }

  // Méthode pour supprimer un test (exemple)
  deleteTest(testId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/tests/${testId}`);
  }
=======
export class EvaluationsService {

  constructor() { }
>>>>>>> a5f00270d44e6bbdd13c6804586b07cb4aa4df06
}
