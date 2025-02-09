import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router'; // <-- Ajoutez cette ligne
import { TestComponent } from './test/test.component';
import { EtudiantComponent } from './etudiant/etudiant.component';
import { ViewprofilComponent } from './etudiant/viewprofil/viewprofil.component';
import { UpdateStudentComponent } from './etudiant/update-student/update-student.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    RouterOutlet, // <-- Ajoutez RouterOutlet ici
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Gestion des Tests TOEIC';
}
