import { Component, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { NavbarComponent } from '../navbar/navbar.component';
import { ClasseService } from '../services/classe.service';

@Component({
  selector: 'app-classe',
  standalone: true,
  templateUrl: './classe.component.html', 
  styleUrls: ['./classe.component.css'],   
  imports: [CommonModule, FormsModule, NavbarComponent]
})
export class ClasseComponent {
  // Propriété pour le formulaire
  classe = { Titre: '', Type: '', Date: '', groupe: '' };

  // Exemple de génération de questions (Listening 1 à 100 et Reading 101 à 200)
  listeningQuestions = Array.from({ length: 100 }, (_, i) => ({ numero: i + 1, reponse: '' }));
  readingQuestions = Array.from({ length: 100 }, (_, i) => ({ numero: i + 101, reponse: '' }));

  // Référence au fichier input caché pour sélectionner le CSV
  @ViewChild('fileInput') fileInput!: ElementRef;

  constructor(private classeService: ClasseService) {} // Assurez-vous que le service existe

  // Méthode appelée par le bouton "Imprimer Liste"
  triggerFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  // Gère le fichier sélectionné
  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      console.log("Fichier sélectionné :", file);
      alert("Fichier CSV sélectionné : " + file.name);
      // Vous pouvez ajouter ici la logique pour traiter le fichier CSV
    }
  }

  // Méthode appelée lors de la soumission du formulaire
  onSubmit() {
    if (!this.classe.Titre || !this.classe.Type || !this.classe.Date || !this.classe.groupe) {
      alert('Veuillez remplir tous les champs avant d’enregistrer !');
      return;
    }
    
    // Combiner les questions Listening et Reading
    const classeData = { 
      ...this.classe, 
      listeningQuestions: this.listeningQuestions, 
      readingQuestions: this.readingQuestions 
    };
    
    // Vous pouvez appeler votre service pour enregistrer la classe
    // this.classeService.addClasse(classeData).subscribe(...);
    alert('Classe enregistrée !');
  }
}
