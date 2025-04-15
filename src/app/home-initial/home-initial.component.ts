import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-home-initial',
  templateUrl: './home-initial.component.html',
  styleUrls: ['./home-initial.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule, NavbarComponent]
})
export class HomeInitialComponent {
  // Données pour les statistiques
  stats = [
    { value: '1000+', label: 'Étudiants évalués' },
    { value: '50+', label: 'Tests disponibles' },
    { value: '95%', label: 'Taux de réussite' },
    { value: '24/7', label: 'Support disponible' }
  ];

  // Fonctionnalités principales
  features = [
    {
      title: 'Évaluations TOEIC',
      description: 'Gérez et passez vos tests TOEIC en toute simplicité',
      icon: '📝',
      link: '/evaluations'
    },
    {
      title: 'Gestion des Étudiants',
      description: 'Gérez les profils et suivez les résultats des étudiants',
      icon: '👥',
      link: '/students'
    },
    {
      title: 'Gestion des Classes',
      description: 'Organisez vos groupes et promotions',
      icon: '🏫',
      link: '/classes'
    }
  ];
} 