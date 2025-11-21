import lcs
import moss

merge_git = """
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i]; i++;
        } else {
            arr[k] = R[j]; j++;
        }
        k++;
    }
    while (i < n1) { arr[k] = L[i]; i++; k++; }
    while (j < n2) { arr[k] = R[j]; j++; k++; }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}
"""


# merge_changing_workflow = """
# void merge(vector<int>& arr, int left, int mid, int right) {
#
#     int n2 = right - mid;
#     int n1 = mid - left + 1;
#     vector<int> L(n1), R(n2);
#
#     for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];
#     for (int i = 0; i < n1; i++) L[i] = arr[left + i];
#
#     int j = 0, i = 0, k = left;
#     while (j < n2 && i < n1) {
#         if (L[i] > R[j]) {
#             arr[k] = R[j]; j++;
#         } else {
#             arr[k] = L[i]; i++;
#         }
#         k++;
#     }
#     while (j < n2) { arr[k] = R[j];
#     j++;
#      k++; }
#     while (i < n1) { arr[k] = L[i];
#     i++;
#     k++; }
# }
#
# void mergeSort(vector<int>& arr, int left, int right) {
#     if (left >= right) return;
#     int mid = left + (right - left) / 2;
#     mergeSort(arr, left, mid);
#     mergeSort(arr, mid + 1, right);
#     merge(arr, left, mid, right);
# }
# """

lele= """
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1, n2;
    int i, j, k;

    
    while (true) {
        n1 = mid - left + 1;
        n2 = right - mid;
        vector<int> L(n1), R(n2);

        
        for (j = 0; j < n2; j++) {
            R[j] = arr[mid + 1 + j];
        }

        
        for (i = 0; i < n1; i++) {
            L[i] = arr[left + i];
        }

        i = 0; j = 0; k = left;

       
        while (true) {
            if (i >= n1 && j >= n2) break;

            if (j >= n2) {          
                arr[k] = L[i]; i++;
            } 
            else if (i >= n1) {     
                arr[k] = R[j]; j++;
            } 
            else if (R[j] < L[i]) { 
                arr[k] = R[j]; j++; 
            } 
            else {
                arr[k] = L[i]; i++;
            }
            k++;
        }

        break; 
    }
}

void mergeSort(vector<int>& arr, int left, int right) {
    while (1) {
        if (left >= right) break;
        
        int mid = left + (right - left) / 2;

       
        mergeSort(arr, mid + 1, right); 
        mergeSort(arr, left, mid);     

        merge(arr, left, mid, right);
        
        break;
    }
}
"""

mos = moss.MossDetector.compute_similarity(merge_git, lele, "cc", "merge_sort", "merge_sort_with_changed_workflow" )
print(mos)
spr = lcs.compute_lcs(merge_git, lele)
print(spr)

# Modyfikacja kodu polegająca na zmianie kolejności niezależnych bloków instrukcji oraz opakowaniu logiki w sztuczne pętle sterujące zredukowała wskaźnik podobieństwa z poziomu plagiatu do zaledwie 15% (wartość poniżej progu szumu statystycznego).
#
# Jednocześnie wysoki wynik algorytmu LCS (75%) dowodzi, że semantyka i słownictwo kodu pozostały niemal nienaruszone. Oznacza to, że MOSS, polegając na lokalnej spójności strukturalnej, generuje fałszywe wyniki negatywne (False Negatives) w przypadku, gdy student zastosuje proste techniki inżynierii kodu, które nie wymagają zaawansowanej wiedzy programistycznej.