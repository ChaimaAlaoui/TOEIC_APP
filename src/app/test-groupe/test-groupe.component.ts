// test-groupe.component.ts

import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-test-groupe',
  templateUrl: './test-groupe.component.html',
  styleUrls: ['./test-groupe.component.css'],
  imports: [CommonModule, FormsModule]

})

export class TestGroupeComponent implements OnInit {

  searchTerm: string = '';

  groupes = [
    {
      id_groupe: 1,
      nom: 'Groupe Alpha',
      description: 'Un groupe de test avec une description aléatoire.',
      titre: 'Projet Alpha',
      nombre_evaluation: 3,
      nombre_etudiant: 15,
      selected: false
    },
    {
      id_groupe: 2,
      nom: 'Groupe Beta',
      description: 'Deuxième groupe pour vérifier le rendu.',
      titre: 'Sujet Beta',
      nombre_evaluation: 5,
      nombre_etudiant: 12,
      selected: false
    },
    {
      id_groupe: 3,
      nom: 'Groupe Gamma',
      description: 'Dernier groupe de test avec plus d\'étudiants.',
      titre: 'Thème Gamma',
      nombre_evaluation: 2,
      nombre_etudiant: 20,
      selected: false
    }
  ];

  get filteredGroupes() {
    if (!this.searchTerm) return this.groupes;
    return this.groupes.filter(g =>
      g.nom.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  constructor() {}

  ngOnInit(): void {}

  onSubmitSelection() {
    const selectedGroupes = this.groupes.filter(g => g.selected);
    console.log('Groupes sélectionnés :', selectedGroupes);
    alert(`Vous avez sélectionné ${selectedGroupes.length} groupe(s).`);
  }

}
