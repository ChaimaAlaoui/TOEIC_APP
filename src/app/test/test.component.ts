import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { TestCreationService } from '../services/testcreation.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http'; // Importer HttpClient pour récupérer les données
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-test',
  standalone: true,
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css'],
  imports: [CommonModule, FormsModule, RouterModule, NavbarComponent]
})
export class TestComponent implements OnInit {

  test = {
    Titre: '',
    Description: '',
    Site: '',
    Date: ''
  };
  
  selectedGroups: number[] = [];
  responses: { num_question: string, choix: string }[] = [];
  sites: { id: number, nom: string }[] = [];
  
  constructor(
    private testCreationService: TestCreationService,
    private router: Router,
    private http: HttpClient // Injecter HttpClient
  ) {}

  ngOnInit(): void {
    // Récupérer les données du test depuis le service
    const storedTest = this.testCreationService.getTestData();
    this.fetchSites();  // Charger les sites au démarrage
    if (storedTest) {
      this.test = storedTest;
    }
    
    // Récupérer les groupes sélectionnés
    this.selectedGroups = this.testCreationService.getSelectedGroupes();
    
    // Récupérer les réponses configurées
    this.responses = this.testCreationService.getReponses();
  }
// Méthode pour récupérer les sites depuis l'API
fetchSites(): void {
  fetch('http://localhost:5000/api/sitesachraf')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur de réseau');
      }
      return response.json();
    })
    .then(data => {
      this.sites = data; // Remplir le tableau des sites avec les données récupérées
      console.log('Sites récupérés:', this.sites);
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des sites', error);
    });
}


  onConfigureReponses(): void {
    this.testCreationService.setTestData(this.test);
    this.router.navigate(['/reponsejuste']);
  }

  onSaveTest(): void {
    if (!this.test.Titre || !this.test.Date) {
      alert('Veuillez remplir au moins le titre et la date du test');
      return;
    }
  
    if (this.selectedGroups.length === 0) {
      alert('Veuillez sélectionner au moins un groupe');
      return;
    }
  
    if (this.responses.length === 0) {
      alert('Veuillez configurer les réponses du test');
      return;
    }
  
    const testData = {
      nom: this.test.Titre,
      description: this.test.Description,
      date: this.test.Date,
      site: this.test.Site,
    };
  
    const requestBody = {
      test_data: testData,
      test_responses: this.responses,
      selected_groups: this.selectedGroups
    };
  
    console.log("Données envoyées :", requestBody.test_data);
    console.log("Données envoyées :", requestBody.selected_groups);
    console.log("Données envoyées :", requestBody.selected_groups);
  
    fetch('http://127.0.0.1:5000/api/tests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        alert('Test enregistré avec succès');
        this.testCreationService.clearAll();
        this.test = { Titre: '', Description: '', Site: '', Date: '' };
        this.selectedGroups = [];
        this.responses = [];

        this.router.navigate(['/evaluations']);
      } else {
        alert(`Erreur: ${result.error || 'Erreur inconnue'}`);
      }
    })
    .catch(error => {
      console.error('Erreur:', error);
      alert('Erreur lors de l\'enregistrement du test');
    });
  }

  selectionnerClasse(): void {
    this.testCreationService.setTestData(this.test);
    console.log(this.test);
    this.router.navigate(['/classes']);
  }
}
