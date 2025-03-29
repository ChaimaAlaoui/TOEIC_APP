import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-impression',
  templateUrl: './impression.component.html',
  styleUrls: ['./impression.component.css'],
  imports: [FormsModule, CommonModule, NavbarComponent]
})
export class ImpressionComponent {
  // Méthode qui déclenche l'impression de la page
  printPDF(): void {
    window.print();
  }
}
