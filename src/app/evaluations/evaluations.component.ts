import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../navbar/navbar.component';

interface Evaluation {
  id: number;
  titre: string;
  description: string;
  date: string;
  groupe:String;
}

@Component({
  selector: 'app-evaluations',
  templateUrl: './evaluations.component.html',
  styleUrls: ['./evaluations.component.css'],
  imports: [FormsModule, CommonModule, NavbarComponent]
})
export class EvaluationsComponent implements OnInit {
  evaluations: Evaluation[] = [];
  // Propriété liée à l'input de recherche
  searchTerm: string = '';

  ngOnInit(): void {
    // Remplacez par vos données réelles si nécessaire
    this.evaluations = [
      { id: 1, titre: 'Évaluation TOEIC 1', description: 'Description 1', date: "01/04/2023" ,groupe:"1"},
      { id: 2, titre: 'Évaluation TOEIC 2', description: 'Description 2', date: "04/04/2024", groupe:"1" },
      { id: 3, titre: 'Test TOEIC Avancé', description: 'Description avancée', date: "10/05/2023" ,groupe:"1"},
      { id: 4, titre: 'Évaluation TOEIC Standard', description: 'Description standard', date: "15/06/2023",groupe:"1"  },
      { id: 5, titre: 'test 1', description: 'descripti1', date: "19/03/2025",groupe:"1" },
      // Ajoutez d'autres évaluations si besoin
    ];
  }

  // Getter pour retourner les évaluations filtrées en fonction du terme de recherche
  get filteredEvaluations(): Evaluation[] {
    if (!this.searchTerm.trim()) {
      return this.evaluations;
    }
    return this.evaluations.filter(evaluation =>
      evaluation.titre.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  deleteEvaluation(id: number): void {
    this.evaluations = this.evaluations.filter(evaluation => evaluation.id !== id);
  }

  duplicateEvaluation(id: number): void {
    const evalToDuplicate = this.evaluations.find(evaluation => evaluation.id === id);
    if (evalToDuplicate) {
      const newEvaluation: Evaluation = { ...evalToDuplicate, id: Date.now() };
      this.evaluations.push(newEvaluation);
    }
  }
}
