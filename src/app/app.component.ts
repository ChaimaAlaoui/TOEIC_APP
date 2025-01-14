import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { TestComponent } from './test/test.component';

// Interface pour représenter un test

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, CommonModule, TestComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})



export class AppComponent {
  title = 'Gestion des Tests TOEIC';
}
