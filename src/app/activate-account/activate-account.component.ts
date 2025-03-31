import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-activate-account',
  templateUrl: './activate-account.component.html',
  styleUrls: ['./activate-account.component.css'],
  imports: [FormsModule, CommonModule],
})
export class ActivateAccountComponent implements OnInit {
  statusMessage: string = '';
  messageType: string = '';
  loading: boolean = true;
  token: string = '';

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    // Simuler un délai de chargement pour montrer l'animation
    setTimeout(() => {
      this.token = this.route.snapshot.paramMap.get('token') || '';
      if (this.token) {
        this.activateAccount(this.token);
      } else {
        this.loading = false;
        this.statusMessage = 'Aucun token d\'activation trouvé.';
        this.messageType = 'error';
      }
    }, 1500); // Délai de 1.5 seconde pour afficher l'animation de chargement
  }

  activateAccount(token: string) {
    fetch(`http://127.0.0.1:5000/api/activate/${token}`)
      .then((response) => response.json())
      .then((data) => {
        this.loading = false;
        if (data.status === 'success') {
          this.statusMessage = 'Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter et accéder à toutes les fonctionnalités de notre plateforme.';
          this.messageType = 'success';
        } else {
          this.statusMessage = data.message || 'Le lien d\'activation est invalide ou a expiré. Veuillez contacter le support si vous avez besoin d\'aide.';
          this.messageType = 'error';
        }
      })
      .catch((error) => {
        this.loading = false;
        this.statusMessage = 'Une erreur est survenue lors de l\'activation du compte. Veuillez réessayer ultérieurement ou contacter le support.';
        this.messageType = 'error';
        console.error('Erreur d\'activation:', error);
      });
  }

  navigateToLogin() {
    this.router.navigate(['/login']);
  }

  tryAgain() {
    this.loading = true;
    setTimeout(() => {
      if (this.token) {
        this.activateAccount(this.token);
      } else {
        this.loading = false;
        this.statusMessage = 'Aucun token d\'activation trouvé.';
      }
    }, 1000);
  }

  navigateToHome() {
    this.router.navigate(['/']);
  }
}