// Composant d'impression autonome qui génère et affiche le PDF
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-impression',
  templateUrl: './impression.component.html',
  styleUrls: ['./impression.component.css'],
  standalone: true,
  imports: [CommonModule, NavbarComponent]
})
export class ImpressionComponent implements OnInit, OnDestroy {
  pdfUrl: SafeResourceUrl | null = null;
  testId: number | null = null;
  groupeId: number | null = null;
  isLoading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    // Récupérer les paramètres de l'URL
    this.testId = Number(this.route.snapshot.paramMap.get('testId'));
    this.groupeId = Number(this.route.snapshot.paramMap.get('groupeId'));
    
    // Générer et afficher le PDF directement
    this.generateAndDisplayPdf();
  }

  generateAndDisplayPdf(): void {
    if (!this.testId || !this.groupeId) {
      console.error('IDs de test ou de groupe manquants');
      this.isLoading = false;
      return;
    }

    // Appel à l'API pour générer le PDF
    fetch(`http://localhost:5000/api/generateresponsesheet/${this.testId}/${this.groupeId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur lors de la génération du PDF');
        }
        return response.blob();
      })
      .then(blob => {
        // Créer une URL pour le blob et l'utiliser dans l'iframe
        const objectUrl = URL.createObjectURL(blob);
        this.pdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        
        // Stocker l'URL dans une propriété pour pouvoir la nettoyer plus tard
        this._objectUrl = objectUrl;
        
        this.isLoading = false;
      })
      .catch(error => {
        console.error('Erreur:', error);
        alert('Impossible de générer la fiche de réponse. Veuillez réessayer plus tard.');
        this.isLoading = false;
      });
  }

  // URL de l'objet pour le nettoyage
  private _objectUrl: string | null = null;

  printPDF(): void {
    window.print();
  }

  ngOnDestroy(): void {
    // Nettoyer l'URL de l'objet si elle existe
    if (this._objectUrl) {
      URL.revokeObjectURL(this._objectUrl);
    }
  }

  // Ajoutez cette méthode dans votre ImpressionComponent
downloadPDF(): void {
  if (!this.testId || !this.groupeId) return;
  
  // Afficher un état de téléchargement si nécessaire
  let isDownloading = true;
  
  fetch(`http://localhost:5000/api/generateresponsesheet/${this.testId}/${this.groupeId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors du téléchargement du PDF');
      }
      return response.blob();
    })
    .then(blob => {
      // Créer un lien pour télécharger le fichier
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `fiche_reponse_test_${this.testId}_groupe_${this.groupeId}.pdf`;
      document.body.appendChild(a);
      a.click();
      
      // Nettoyer
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    })
    .catch(error => {
      console.error(error);
      alert('Impossible de télécharger la fiche de réponse. Veuillez réessayer plus tard.');
    })
    .finally(() => {
      // Réinitialiser l'état de téléchargement si nécessaire
      isDownloading = false;
    });
}
}