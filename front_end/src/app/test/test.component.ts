import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TestService } from '../test.service';

@Component({
  selector: 'app-test',
  standalone: true,
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css'],
  imports: [CommonModule, FormsModule]
})
export class TestComponent {
  test = { Titre: '', Type: '', Date: '', groupe: '' };
  
  // ✅ Définition de `questions` avec 200 entrées vides
  questions = Array.from({ length: 200 }, (_, i) => ({ numero: i + 1, reponse: '' }));

  constructor(private testService: TestService) {} 

  onSubmit() {

    if (!this.test.Titre || !this.test.Type || !this.test.Date || !this.test.groupe) {
      alert('Veuillez remplir tous les champs avant d’enregistrer !');
      return;
    }
    const testData = { ...this.test, questions: this.questions };
    this.testService.createTest(testData).subscribe(response => {
      alert('Test enregistré avec succès !');
    }, error => {
      console.error('Erreur lors de l’enregistrement', error);
    });
  }
}




