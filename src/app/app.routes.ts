import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ActivateAccountComponent } from './activate-account/activate-account.component';
import { TestComponent } from './test/test.component';
import { HomeComponent } from './home/home.component';
import { ClasseComponent } from './classe/classe.component';
import { EvaluationsComponent } from './evaluations/evaluations.component';

import { ReponseEtudiantComponent } from './reponseetudiant/reponseetudiant.component';
import { ImpressionComponent } from './impression/impression.component';
import { ReponseJusteComponent } from './reponsejuste/reponsejuste.component';
import { TestGroupeComponent } from './test-groupe/test-groupe.component';



export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' } ,
  { path: 'activate-account/:token', component: ActivateAccountComponent },
  { path: 'test', component: TestComponent },
  { path: 'home', component: HomeComponent },
  { path: 'classe', component: ClasseComponent },
  { path: 'evaluations', component: EvaluationsComponent },
  { path: 'classes', component: TestGroupeComponent },
  { path: 'reponseetudiant', component: ReponseEtudiantComponent },
  { path: 'impression', component: ImpressionComponent },
  { path: 'reponsejuste', component: ReponseJusteComponent },

];
