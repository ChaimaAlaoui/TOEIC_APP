import { CommonModule } from '@angular/common';
import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NavbarComponent } from '../navbar/navbar.component';
import { NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';


interface TestGroupe {
  test_id: number;
  test_title: string;
  test_date: string;  // Add this line
  test_description: string;  // Add this line
  groupe_id: number;
  groupe_name: string;
  feuille_generee: boolean;  // Add this line for feuille_generee status
}

interface StudentResult {
  [studentNumber: string]: string[]; // Les réponses des étudiants, chaque étudiant ayant un tableau de réponses
}


@Component({
  selector: 'app-evaluations',
  templateUrl: './evaluations.component.html',
  styleUrls: ['./evaluations.component.css'],
  imports: [FormsModule, CommonModule, NavbarComponent, NgbModule  ]
})
export class EvaluationsComponent implements OnInit {

  testsAndGroups: TestGroupe[] = [];
  searchTerm: string = '';
  isLoading: boolean | undefined;
  http: any;
  loadingButtonId: string | null = null;
  @ViewChild('uploadModal') uploadModal: TemplateRef<any> | undefined;
  selectedEvaluation: any; 

  constructor(private modalService: NgbModal,private router: Router) {}

  
  showModal = false;

  openUploadModal(evaluation: any) {
    this.selectedEvaluation = evaluation;
    this.showModal = true;
  }


 

  // Méthode pour gérer le changement de fichier
  onFileChange(event: any) {
    const file = event.target.files[0];
    // Logique pour gérer le fichier
  }

  // Méthode pour soumettre le formulaire
  onSubmit() {
    if (!this.isLoading) {
      this.isLoading = true;
      
      // Logique pour traiter et téléverser le fichier
      
      // Simuler la fin du téléversement
      setTimeout(() => {
        this.isLoading = false;
        // Ajouter un traitement supplémentaire si nécessaire
      }, 2000);
    }
  }


  ngOnInit(): void {
    this.getTestsAndGroups();
  }

  getTestsAndGroups(): void {
    fetch('http://localhost:5000/api/evaluations') 
      .then(response => response.json())
      .then(data => {
        this.testsAndGroups = data;
      })
      .catch(error => console.error('Error fetching tests and groups:', error));
  }
  

  // Getter pour les évaluations filtrées
 // Getter pour les évaluations filtrées
get filteredEvaluations(): TestGroupe[] {
  let result: TestGroupe[];
  
  if (!this.searchTerm.trim()) {
    result = this.testsAndGroups;
  } else {
    result = this.testsAndGroups.filter(item =>
      item.test_title.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
  
  // Afficher les données dans la console
  // console.log('Évaluations filtrées:', result);
  
  // Vérifier spécifiquement la propriété feuille_generee
 
  
  return result;
}
// Au lieu de this.isLoading = true/false
// Utilisez une variable pour stocker l'ID du bouton en cours de chargement
 // Cette méthode redirige vers le composant d'impression avec les IDs en paramètres
 viewResponseSheet(testId: number, groupeId: number) {
  // Définir quel bouton est en chargement
  this.loadingButtonId = `btn-${testId}-${groupeId}`;
  
  // Rediriger vers le composant d'impression avec les paramètres
  this.router.navigate(['/impression', testId, groupeId]);
  
  // Réinitialiser le statut du bouton
  setTimeout(() => {
    this.loadingButtonId = null;
  }, 500);
}
  // Suppression de l'évaluation
  deleteEvaluation(id: number): void {
    this.testsAndGroups = this.testsAndGroups.filter(evaluation => evaluation.test_id !== id);
  }

  // Dupliquer une évaluation
  duplicateEvaluation(id: number): void {
    const evalToDuplicate = this.testsAndGroups.find(evaluation => evaluation.test_id === id);
    if (evalToDuplicate) {
      const newEvaluation: TestGroupe = { ...evalToDuplicate, test_id: Date.now() };
      this.testsAndGroups.push(newEvaluation);
    }
  }

  uploadPdf(testId: string, groupeId: string): void {
    // Désactiver le bouton pendant le téléversement
    this.isLoading = true;
  
    // Vérifier les paramètres obligatoires
    if (!testId || !groupeId) {
      alert('Les identifiants de test et de groupe sont requis');
      this.isLoading = false;
      return;
    }

    // Obtenir le fichier depuis l'input
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    const file = fileInput?.files?.[0];
  
    if (!file) {
      alert('Veuillez sélectionner un fichier PDF');
      this.isLoading = false;
      return;
    }

    // Vérifier que c'est bien un PDF
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert('Veuillez sélectionner un fichier PDF valide');
      this.isLoading = false;
      return;
    }

    console.log(testId);
    console.log(groupeId)
  
    // Créer un FormData pour envoyer le fichier
    const formData = new FormData();
    formData.append('pdf_file', file);
    formData.append('test_id', testId);
    formData.append('groupe_id', groupeId);
  
    // Effectuer la requête fetch vers votre API backend
    fetch('http://localhost:5000/api/process-pdf', {
      method: 'POST',
      body: formData,
      // Ajout de credentials si nécessaire pour les cookies
      // credentials: 'include',
    })
    .then(response => {
      // Traiter la réponse comme JSON même en cas d'erreur HTTP
      return response.json().then(data => {
        if (!response.ok) {
          // Lever une erreur avec les détails du backend si disponibles
          throw new Error(data.error || `Erreur HTTP: ${response.status}`);
        }
        return data;
      });
    })
    .then((data: { message: string; saved_count: number; student_count: number }) => {
      console.log('Résultats du traitement:', data);
      
      // Afficher un message de succès avec les détails
      alert(`${data.message}\nRéponses enregistrées: ${data.saved_count} pour ${data.student_count} étudiants.`);
      
      // Éventuellement, réinitialiser le formulaire ou rafraîchir les données
      fileInput.value = '';
    })
    .catch(error => {
      console.error('Erreur:', error);
      alert(`Erreur: ${error.message}`);
    })
    .finally(() => {
      // Réactiver le bouton
      this.isLoading = false;
    });
}
  
}
