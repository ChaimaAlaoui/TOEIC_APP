import { Injectable } from '@angular/core';
import { Test } from '../models/test.model';
import { ReponseJuste } from '../models/reponse-juste.model';

@Injectable({
  providedIn: 'root'
})
export class TestCreationService {
  private tempTestData: Test | null = null;
  private tempReponses: ReponseJuste[] = [];

  setTestData(test: Test): void {
    this.tempTestData = test;
  }

  getTestData(): Test | null {
    return this.tempTestData;
  }

  setReponses(reponses: ReponseJuste[]): void {
    this.tempReponses = reponses;
  }

  getReponses(): ReponseJuste[] {
    return this.tempReponses;
  }

  clearAll(): void {
    this.tempTestData = null;
    this.tempReponses = [];
  }
}
