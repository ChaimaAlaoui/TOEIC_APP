import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { SuccessDialogComponent } from '../../success-dialog/success-dialog.component';

@Component({
  selector: 'app-addstudent',
  imports: [RouterLink, FormsModule, CommonModule],
  standalone: true,
  templateUrl: './addstudent.component.html',
  styleUrl: './addstudent.component.css'
})
export class AddstudentComponent implements OnInit {
  // Propriétés pour lier les champs du formulaire
  studentLastName = '';
  studentFirstName = '';
  studentPromotionId = '';
  studentGroupId = '';
  studentSiteId = '';
  studentSpecialite = '';
  studentEmail = '';

  // Listes pour les sélections
  promotions: any[] = [];
  groupes: any[] = [];
  sites: any[] = [];
  specialites: any[] = [];

  constructor(private router: Router, private dialog: MatDialog) {}

  ngOnInit() {
    // Charger les listes dès que le composant est monté
    this.fetchPromotions();
    this.fetchGroupes();
    this.fetchSites();
  }

  // Récupération des promotions
  fetchPromotions() {
    fetch('http://localhost:5000/api/promotions')
      .then((res) => res.json())
      .then((data) => {
        // Supprimer les doublons en utilisant un Set basé sur l'ID
        const uniquePromotions = Array.from(new Map(data.map((item: { id: any; }) => [item.id, item])).values());
        this.promotions = uniquePromotions;
      })
      .catch((error) => console.error('Erreur lors du chargement des promotions:', error));
  }
  

  // Récupération des groupes
  fetchGroupes() {
    fetch('http://localhost:5000/api/groupes')
      .then((res) => res.json())
      .then((data) => {
        this.groupes = data;
      })
      .catch((error) => console.error('Erreur lors du chargement des groupes:', error));
  }

  // Récupération des sites
  fetchSites() {
    fetch('http://localhost:5000/api/sites')
      .then((res) => res.json())
      .then((data) => {
        this.sites = data;
      })
      .catch((error) => console.error('Erreur lors du chargement des sites:', error));
  }

  

  // Méthode pour envoyer les données du formulaire avec fetch
  addStudent() {
    console.log('Ajout d’un étudiant:', this.studentLastName, this.studentFirstName, this.studentPromotionId, this.studentGroupId, this.studentSiteId, this.studentSpecialite, this.studentEmail);

    const student = {
      nom: this.studentLastName,
      prenom: this.studentFirstName,
      promotion_id: this.studentPromotionId,
      groupe_id: this.studentGroupId,
      site_id: this.studentSiteId,
      specialite: this.studentSpecialite,
      email: this.studentEmail
    };

    fetch('http://localhost:5000/api/etudiants', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(student)
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Étudiant ajouté avec succès:', data);
        this.dialog.open(SuccessDialogComponent, {
          width: '300px',
          data: { message: 'Étudiant ajouté avec succès !' },
        });

        this.dialog.afterAllClosed.subscribe(() => {
          this.router.navigate(['/studentlist']);
        });
      })
      .catch((error) => {
        console.error('Erreur lors de l’ajout de l’étudiant:', error);
      });
  }
}
