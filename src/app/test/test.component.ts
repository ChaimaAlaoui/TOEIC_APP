import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Test } from '../models/test.model';
import { TestService } from '../services/test.service';
import { TestCreationService } from '../services/testcreation.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReponseJusteService } from '../services/reponsejuste.service';

@Component({
  selector: 'app-test',
  standalone: true,
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css'],
  imports: [CommonModule, FormsModule]
})


export class TestComponent implements OnInit {

  test: Test = {
    Titre: '',
    Description: '',
    Site: '',
    Date: ''
  };
  

  constructor(
    private testService: TestService,
    private testCreationService: TestCreationService,
    private router: Router,
    private reponseJusteService: ReponseJusteService
  ) {}

  ngOnInit(): void {
    // Si un test a été sauvegardé temporairement, le récupérer
    const storedTest = this.testCreationService.getTestData();
    if (storedTest) {
      this.test = storedTest;
    }
  }

  onConfigureReponses(): void {
    // Stocker le test dans le service et naviguer vers la configuration des réponses
    this.testCreationService.setTestData(this.test);
    this.router.navigate(['/reponsejuste']);
  }

  onSaveTest(): void {
    // Récupérer le test temporaire
    const finalTest = this.testCreationService.getTestData() || this.test;
    this.testService.createTest(finalTest).subscribe({
      next: (res: any) => {
        const createdTestId = res.id_test;
        alert('Test créé avec succès ! ID = ' + createdTestId);
        
        // Récupérer les réponses temporairement stockées
        const reponses = this.testCreationService.getReponses();
        // Mettre à jour l'id_test de chaque réponse
        reponses.forEach(r => r.id_test = createdTestId);
        
        // Maintenant, vous pouvez appeler le service pour sauvegarder les réponses en base,
        // par exemple :
        this.reponseJusteService.createReponsesBatch(reponses).subscribe({
          next: (resp) => {
            alert(resp.message);
            // Nettoyage après succès
            this.testCreationService.clearAll();
            this.test = { Titre: '', Description: '', Site: '', Date: '' };
          },
          error: (err) => {
            console.error(err);
            alert('Erreur lors de la sauvegarde des réponses.');
          }
        });
      },
      error: (err) => {
        console.error(err);
        alert('Erreur lors de la création du test.');
      }
    });
  }


  selectionnerClasse() {
    
    this.testCreationService.setTestData(this.test);
    this.router.navigate(['/classes']);
    
      

    
    }
  
}
