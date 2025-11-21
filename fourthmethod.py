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


merge_fake ="""
void merge(vector<long long>& arr, long long left, long long mid, long right) {
    long long n1 = mid - left + 1;
    long long n2 = right - mid;
    
    vector<long long> L(n1), R(n2);

    for (long long i = 0; i < n1; i++) L[i] = arr[left + i];
    for (long long j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    long long i = 0; 
    long long j = 0; 
    long long k = left;

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

void mergeSort(vector<long long>& arr, long long left, long right) {
    if (left >= right) return;
    
    long long mid = left + (right - left) / 2;
    
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}
"""

mos = moss.MossDetector.compute_similarity(merge_git, merge_fake, "cc")
print(mos)
ls = lcs.compute_lcs(merge_git, merge_fake)
print(ls)