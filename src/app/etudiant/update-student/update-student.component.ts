import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { SuccessDialogComponent } from '../../success-dialog/success-dialog.component';

@Component({
  selector: 'app-update-student',
  standalone: true,
  imports: [FormsModule, CommonModule,RouterLink],
  templateUrl: './update-student.component.html',
  styleUrls: ['./update-student.component.css']
})
export class UpdateStudentComponent implements OnInit {
  studentId!: string;
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

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.studentId = this.route.snapshot.paramMap.get('id')!; // Récupère l'ID depuis l'URL
    this.getStudentDetails();
    this.fetchPromotions();
    this.fetchGroupes();
    this.fetchSites();
  }

  // Récupérer les détails de l'étudiant
  getStudentDetails() {
    fetch(`http://localhost:5000/api/etudiants/${this.studentId}`)
      .then((response) => response.json())
      .then((data) => {
        this.studentLastName = data.nom;
        this.studentFirstName = data.prenom;
        this.studentPromotionId = data.promotion_id;
        this.studentGroupId = data.groupe_id;
        this.studentSiteId = data.site_id;
        this.studentSpecialite = data.specialite;
        this.studentEmail = data.email;
      })
      .catch((error) => console.error('Erreur lors de la récupération des détails de l\'étudiant:', error));
  }

  // Récupération des promotions
  fetchPromotions() {
    fetch('http://localhost:5000/api/promotions')
      .then((res) => res.json())
      .then((data) => {
        this.promotions = data;
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

  // Méthode pour mettre à jour l'étudiant
  updateStudent() {
    const updatedStudent = {
      nom: this.studentLastName,
      prenom: this.studentFirstName,
      promotion_id: this.studentPromotionId,
      groupe_id: this.studentGroupId,
      site_id: this.studentSiteId,
      specialite: this.studentSpecialite,
      email: this.studentEmail
    };

    fetch(`http://localhost:5000/api/etudiants/${this.studentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedStudent)
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Étudiant mis à jour avec succès:', data);
        this.dialog.open(SuccessDialogComponent, {
          width: '300px',
          data: { message: 'Étudiant mis à jour avec succès !' },
        });

        this.dialog.afterAllClosed.subscribe(() => {
          this.router.navigate(['/studentlist']);
        });
      })
      .catch((error) => console.error('Erreur lors de la mise à jour de l\'étudiant:', error));
  }
}