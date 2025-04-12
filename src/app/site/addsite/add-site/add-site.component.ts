import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { NavbarComponent } from '../../../navbar/navbar.component';
import { SuccessDialogComponent } from '../../../success-dialog/success-dialog.component';

@Component({
  selector: 'app-add-site',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterLink, NavbarComponent],
  templateUrl: './add-site.component.html',
  styleUrls: ['./add-site.component.css']
})
export class AddSiteComponent {
  siteNom = '';
  errors: any = {};

  constructor(private router: Router, private dialog: MatDialog) {}

  validateForm(): boolean {
    this.errors = {}; // Réinitialise les erreurs

    if (!this.siteNom) {
      this.errors['siteNom'] = 'Le nom du site est requis.';
    } else if (this.siteNom.length > 50) {
      this.errors['siteNom'] = 'Le nom ne doit pas dépasser 50 caractères.';
    }

    return Object.keys(this.errors).length === 0;
  }

  addSite() {
    // Validation du formulaire
    if (!this.validateForm()) {
      return;
    }

    const siteData = {
      nom: this.siteNom
    };

    fetch('http://localhost:5000/api/sites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(siteData)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de l\'ajout du site');
        }
        return response.json();
      })
      .then(data => {
        console.log('Site ajouté avec succès:', data);
        const dialogRef = this.dialog.open(SuccessDialogComponent, {
          width: '300px',
          data: { message: 'Site ajouté avec succès !' }
        });

        dialogRef.afterClosed().subscribe(() => {
          this.router.navigate(['/site']);
        });
      })
      .catch(error => {
        console.error('Erreur:', error);
        this.errors['general'] = 'Une erreur est survenue lors de l\'ajout du site';
      });
  }
}