import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { SuccessDialogComponent } from '../../../success-dialog/success-dialog.component';

@Component({
  selector: 'app-addgroup',
  imports: [RouterLink, FormsModule, CommonModule],
  standalone: true,
  templateUrl: './addgroup.component.html',
  styleUrl: './addgroup.component.css'
})
export class AddGroupComponent implements OnInit {
  groupName = '';
  groupPromotionId = '';
  groupSiteId = '';
  groupSemestreId = '';

  promotions: any[] = [];
  sites: any[] = [];
  semestres: any[] = [];

  filteredPromotions: any[] = [];
  filteredSemestres: any[] = [];

  errors: any = {};

  constructor(private router: Router, private dialog: MatDialog) {}

  ngOnInit() {
    this.fetchSites();
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

  // Récupération des promotions filtrées par site
fetchPromotionsBySite(siteId: string) {
  fetch(`http://localhost:5000/api/promotions/by_site/${siteId}`)
    .then((res) => res.json())
    .then((data) => {
      this.filteredPromotions = data;
    })
    .catch((error) => console.error('Erreur lors du chargement des promotions:', error));
}

// Récupération des semestres filtrés par site et promotion
fetchSemestresBySiteAndPromotion(siteId: string, promotionId: string) {
  fetch(`http://localhost:5000/api/semestres/by_promotion?promotion_id=${promotionId}`)
    .then((res) => res.json())
    .then((data) => {
      this.filteredSemestres = data;
    })
    .catch((error) => console.error('Erreur lors du chargement des semestres:', error));
}

  // Lorsque le site est sélectionné
  onSiteChange(siteId: string) {
    this.groupSiteId = siteId;
    this.groupPromotionId = ''; // Réinitialiser la promotion sélectionnée
    this.groupSemestreId = ''; // Réinitialiser le semestre sélectionné
    this.filteredPromotions = []; // Réinitialiser les promotions filtrées
    this.filteredSemestres = []; // Réinitialiser les semestres filtrés

    if (siteId) {
      this.fetchPromotionsBySite(siteId);
    }
  }

  // Lorsque la promotion est sélectionnée
  onPromotionChange(promotionId: string) {
    this.groupPromotionId = promotionId;
    this.groupSemestreId = ''; // Réinitialiser le semestre sélectionné
    this.filteredSemestres = []; // Réinitialiser les semestres filtrés

    if (promotionId && this.groupSiteId) {
      this.fetchSemestresBySiteAndPromotion(this.groupSiteId, promotionId);
    }
  }

  // Validation du formulaire
  validateForm(): boolean {
    this.errors = {};

    if (!this.groupName) {
      this.errors['groupName'] = 'Le nom du groupe est requis.';
    }
    if (!this.groupPromotionId) {
      this.errors['groupPromotionId'] = 'La promotion est requise.';
    }
    if (!this.groupSiteId) {
      this.errors['groupSiteId'] = 'Le site est requis.';
    }
    if (!this.groupSemestreId) {
      this.errors['groupSemestreId'] = 'Le semestre est requis.';
    }

    return Object.keys(this.errors).length === 0;
  }

  // Ajouter un groupe
  addGroup() {
    if (!this.validateForm()) {
      return;
    }

    const groupe = {
      nom: this.groupName,
      promotion_id: this.groupPromotionId,
      site_id: this.groupSiteId,
      semestre_id: this.groupSemestreId
    };

    console.log('Envoi des données :', groupe);

    fetch('http://localhost:5000/api/groupes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(groupe)
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Groupe ajouté avec succès:', data);
        this.dialog.open(SuccessDialogComponent, {
          width: '300px',
          data: { message: 'Groupe ajouté avec succès !' },
        });

        this.dialog.afterAllClosed.subscribe(() => {
          this.router.navigate(['/groupelist']);
        });
      })
      .catch((error) => {
        console.error('Erreur lors de l’ajout du groupe:', error);
      });
  }
}