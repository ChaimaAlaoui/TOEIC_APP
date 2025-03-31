import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AnimateOnScrollDirective } from '../Directives/animate-on-scroll.directive';
import { NavbarComponent } from '../navbar/navbar.component';
// N'oubliez pas d'importer votre directive si vous travaillez en standalone


@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  imports: [CommonModule, FormsModule, RouterModule, AnimateOnScrollDirective, NavbarComponent]
})
export class HomeComponent {
  darkMode = false;

  services = [
    { title: 'Créer un Test', description: 'Gérez vos tests TOEIC en quelques clics.', icon: 'fas fa-book' },
    { title: 'Gérer les Classes', description: 'Organisez vos groupes d’étudiants.', icon: 'fas fa-users' },
    { title: 'Suivi des Évaluations', description: 'Analysez la progression des étudiants.', icon: 'fas fa-chart-line' },
    { title: 'Importer les Copies', description: 'Importez et corrigez automatiquement les réponses.', icon: 'fas fa-upload' },
    { title: 'Impression', description: 'Imprimez les feuilles de réponses.', icon: 'fas fa-print' }
  ];

  toggleDarkMode() {
    this.darkMode = !this.darkMode;
    document.body.classList.toggle('dark-mode', this.darkMode);
  }
}
