import { Component, OnInit } from '@angular/core';
import { ReponseJuste } from '../models/reponse-juste.model';

import { Router } from '@angular/router';
import { TestCreationService } from '../services/testcreation.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-reponse-juste',
  templateUrl: './reponsejuste.component.html',
  styleUrls: ['./reponsejuste.component.css'],
  imports: [CommonModule, FormsModule]
})
export class ReponseJusteComponent implements OnInit {
  configQuestions: ReponseJuste[] = [];

  constructor(
    private testCreationService: TestCreationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    
    for (let i = 1; i <= 200; i++) {
      this.configQuestions.push({
        numero_question: i,
        choix: 'A',
        id_test: 0  
      });
    }
  }

  onSaveConfig(): void {
    // Stocker la configuration des réponses dans le service
    this.testCreationService.setReponses(this.configQuestions);
    alert('Configuration des réponses enregistrée localement. Retournez à la page Test pour finaliser.');
    this.router.navigate(['/test']);
  }
}
